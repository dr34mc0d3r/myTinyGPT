import os
import time
import math
import torch
import plotext as pl
from torch.utils.tensorboard import SummaryWriter
from typing import Optional, List

from app.llm.model import TinyTransformer
from app.config.config import Config, ModelConfig, TrainingConfig
from app.tokenizer.processor import TokenizerProcessor
from app.training.dataset import create_dataloader

class Trainer:
    """
    Main training pipeline for the Tiny Transformer.
    """
    def __init__(self, config: Config, device: str = "cpu"):
        self.config = config
        self.device = device
        
        # Load tokenizer
        tokenizer_path = "ai_system/models/tokenizer/tokenizer.model"
        self.tokenizer = TokenizerProcessor(tokenizer_path)
        
        # Adjust vocab size in config if it doesn't match tokenizer
        if self.config.model.vocab_size != self.tokenizer.vocab_size:
            print(f"Adjusting config vocab_size from {self.config.model.vocab_size} to {self.tokenizer.vocab_size}")
            self.config.model.vocab_size = self.tokenizer.vocab_size
            
        # Initialize model
        self.model = TinyTransformer(self.config.model).to(self.device)
        
        # Optimizer
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=self.config.training.learning_rate,
            betas=(self.config.training.beta1, self.config.training.beta2),
            weight_decay=self.config.training.weight_decay
        )
        
        # TensorBoard
        self.writer = SummaryWriter(log_dir="data/logs")
        
        # Plotting buffers
        self.iters: List[int] = []
        self.losses: List[float] = []
        self.lrs: List[float] = []
        self.val_iters: List[int] = []
        self.val_losses: List[float] = []
        
    def get_lr(self, it: int) -> float:
        """
        Cosine learning rate decay with warmup.
        """
        conf = self.config.training
        # 1) linear warmup for warmup_iters steps
        if it < conf.warmup_iters:
            return conf.learning_rate * it / conf.warmup_iters
        # 2) if it > lr_decay_iters, return min learning rate
        if it > conf.lr_decay_iters:
            return conf.min_lr
        # 3) in between, use cosine decay down to min learning rate
        decay_ratio = (it - conf.warmup_iters) / (conf.lr_decay_iters - conf.warmup_iters)
        assert 0 <= decay_ratio <= 1
        coeff = 0.5 * (1.0 + math.cos(math.pi * decay_ratio)) # coeff ranges 0..1
        return conf.min_lr + coeff * (conf.learning_rate - conf.min_lr)

    def train(self, train_path: str, val_path: Optional[str] = None):
        print(f"Starting training on {self.device}...")
        
        # Setup data loaders
        train_loader = create_dataloader(
            train_path,
            self.tokenizer,
            self.config.model.block_size,
            self.config.training.batch_size,
            shuffle=True
        )
        
        val_loader = None
        if val_path is not None:
            val_loader = create_dataloader(
                val_path,
                self.tokenizer,
                self.config.model.block_size,
                self.config.training.batch_size,
                shuffle=False
            )
            print(f"Using validation dataset at {val_path}")
        
        train_iter = iter(train_loader)
        
        best_val_loss = float('inf')
        t0 = time.time()
        
        for it in range(self.config.training.max_iters):
            # Update learning rate
            lr = self.get_lr(it)
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = lr
                
            # Get batch
            try:
                x, y = next(train_iter)
            except StopIteration:
                train_iter = iter(train_loader)
                x, y = next(train_iter)
                
            x, y = x.to(self.device), y.to(self.device)
            
            # Forward pass
            logits, loss = self.model(x, y)
            
            # Backward pass
            self.model.zero_grad(set_to_none=True)
            loss.backward()
            
            # Gradient clipping
            if self.config.training.grad_clip != 0.0:
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.training.grad_clip)
                
            self.optimizer.step()
            
            # Timing and logging
            t1 = time.time()
            dt = t1 - t0
            t0 = t1
            
            if it % self.config.training.log_interval == 0:
                lossf = loss.item()
                self.iters.append(it)
                self.losses.append(lossf)
                self.lrs.append(lr)
                
                print(f"iter {it}: loss {lossf:.4f}, time {dt*1000:.2f}ms, lr {lr:e}")
                self.writer.add_scalar("Loss/train", lossf, it)
                self.writer.add_scalar("LR", lr, it)

                # Generate samples from multiple JavaScript prompts
                self.model.eval()
                prompts = [
                    "function fetchData(",
                    "Array.prototype.map",
                    "async function getUser(",
                    "const promise = new Promise",
                    "document.addEventListener('click', ",
                    "The Map object allows you to ",
                ]
                samples = []
                for p in prompts:
                    sample_continuation = self.generate_text_sample(p, max_new_tokens=50, temperature=0.8, top_k=40)
                    samples.append((p, sample_continuation))
                self.model.train()
                
                # Plot with text in the top half and loss in the lower half
                pl.clf()
                pl.subplots(2, 1)

                pl.subplot(1, 1)
                pl.title("Log + Sample Generation")
                pl.text(f"iter {it}: loss {lossf:.4f}", 1, 1)
                if self.val_losses:
                    pl.text(f"val {self.val_losses[-1]:.4f}", 1, 2)
                
                line_idx = 4
                for prompt, continuation in samples:
                    pl.text(f"Prompt: {prompt[:30]}...", 1, line_idx)
                    cont_lines = [continuation[i:i+55] for i in range(0, min(len(continuation), 110), 55)]
                    for cont_line in cont_lines:
                        line_idx += 1
                        pl.text(f"  {cont_line}", 1, line_idx)
                    line_idx += 1

                pl.subplot(2, 1)
                pl.plot(self.iters, self.losses, label="Train Loss")
                if self.val_iters and self.val_losses:
                    pl.plot(self.val_iters, self.val_losses, label="Val Loss")
                lr_log_values = [math.log10(x) if x > 0 else -10.0 for x in self.lrs]
                pl.plot(self.iters, lr_log_values, label="log10 LR")
                pl.title("Train / Val Loss + log10(LR)")
                pl.text(f"LR shown as log10 scale", 1, 1)

                pl.show()

            # Evaluation
            if it > 0 and it % self.config.training.eval_interval == 0:
                self.model.eval()
                eval_loader = val_loader if val_loader is not None else train_loader
                val_loss = self.estimate_loss(eval_loader)
                print(f"step {it}: val loss {val_loss:.4f}")
                self.writer.add_scalar("Loss/val", val_loss, it)
                self.val_iters.append(it)
                self.val_losses.append(val_loss)
                
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    self.save_checkpoint(it, val_loss, tag="best")
                
                self.model.train()
                
            if it > 0 and it % 1000 == 0:
                self.save_checkpoint(it, loss.item(), tag=f"iter_{it}")

        self.writer.close()
        print("Training complete.")

    @torch.no_grad()
    def estimate_loss(self, loader):
        out = {}
        self.model.eval()
        losses = torch.zeros(self.config.training.eval_iters)
        loader_iter = iter(loader)
        for k in range(self.config.training.eval_iters):
            try:
                x, y = next(loader_iter)
            except StopIteration:
                loader_iter = iter(loader)
                x, y = next(loader_iter)
            x, y = x.to(self.device), y.to(self.device)
            _, loss = self.model(x, y)
            losses[k] = loss.item()
        return float(losses.mean().item())

    @torch.no_grad()
    def generate_text_sample(self, prompt: str, max_new_tokens: int = 30, temperature: float = 1.0, top_k: int | None = None) -> str:
        prompt_ids = self.tokenizer.encode(prompt)
        idx = torch.tensor([prompt_ids], dtype=torch.long, device=self.device)
        generated_ids = self.model.generate(idx, max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k)
        # decode the full generated sequence so the prompt and continuation are visible
        return self.tokenizer.decode(generated_ids[0].tolist())

    def save_checkpoint(self, it: int, loss: float, tag: str = ""):
        checkpoint = {
            'model': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'model_config': self.config.model,
            'training_config': self.config.training,
            'iter': it,
            'loss': loss,
        }
        ckpt_dir = self.config.training.checkpoint_dir
        os.makedirs(ckpt_dir, exist_ok=True)
        path = os.path.join(ckpt_dir, f"ckpt_{tag}.pt")
        print(f"Saving checkpoint to {path}")
        torch.save(checkpoint, path)

if __name__ == "__main__":
    # Load configuration from default
    config = Config()
    
    trainer = Trainer(config)
    trainer.train("ai_system/data/raw/sample_corpus.txt")
