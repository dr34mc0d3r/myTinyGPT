import os
import torch
from typing import Optional, List

from app.llm.model import TinyTransformer
from app.config.config import ModelConfig
from app.tokenizer.processor import TokenizerProcessor

class Generator:
    """
    High-level utility for generating text using a trained Tiny Transformer.
    """
    def __init__(self, checkpoint_path: str, tokenizer_path: str, device: str = "cpu"):
        self.device = device
        
        # Load tokenizer
        self.tokenizer = TokenizerProcessor(tokenizer_path)
        
        # Load checkpoint
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Checkpoint not found at {checkpoint_path}")
            
        print(f"Loading checkpoint from {checkpoint_path}...")
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
        
        # Initialize model from checkpoint config
        model_config = checkpoint.get('model_config')
        if model_config is None:
            # Fallback if config wasn't saved (though trainer.py does save it)
            print("Warning: model_config not found in checkpoint. Using default.")
            model_config = ModelConfig(vocab_size=self.tokenizer.vocab_size)
            
        self.model = TinyTransformer(model_config)
        self.model.load_state_dict(checkpoint['model'])
        self.model.to(device)
        self.model.eval()
        
        print("Model loaded and ready for inference.")

    @torch.no_grad()
    def generate(
        self, 
        prompt: str, 
        max_new_tokens: int = 100, 
        temperature: float = 0.7, 
        top_k: Optional[int] = None
    ) -> str:
        """
        Generates text starting from a prompt, returning only the new tokens.
        """
        # Encode prompt
        idx_input = torch.tensor(self.tokenizer.encode(prompt, add_bos=True), dtype=torch.long, device=self.device).unsqueeze(0)
        prompt_length = idx_input.size(1)
        
        # Generate tokens
        generated_idx = self.model.generate(idx_input, max_new_tokens, temperature=temperature, top_k=top_k)
        
        # Extract only the new tokens
        new_tokens = generated_idx[0, prompt_length:].tolist()
        
        # Decode and return
        return self.tokenizer.decode(new_tokens)

if __name__ == "__main__":
    # Test inference
    checkpoint = "models/checkpoints/ckpt_best.pt"
    tokenizer = "models/tokenizer/tokenizer.model"
    
    if os.path.exists(checkpoint):
        generator = Generator(checkpoint, tokenizer)
        
        prompts = [
            "AI engineering is",
            "The tiny transformer",
            "SentencePiece is"
        ]
        
        for prompt in prompts:
            print(f"\nPrompt: {prompt}")
            output = generator.generate(prompt, max_new_tokens=20, temperature=0.8, top_k=5)
            print(f"Generated: {output}")
    else:
        print("Checkpoint not found. Run training first.")
