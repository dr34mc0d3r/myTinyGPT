import yaml
import os
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class ModelConfig:
    """Configuration for the Tiny Transformer model."""
    vocab_size: int = 8000
    n_layers: int = 12
    n_heads: int = 8
    n_embd: int = 256
    block_size: int = 256  # Context length
    dropout: float = 0.1
    bias: bool = True  # True: bias in Linears and LayerNorms, like GPT-2

@dataclass
class TrainingConfig:
    """Configuration for the training pipeline."""
    batch_size: int = 8
    gradient_accumulation_steps: int = 8
    learning_rate: float = 6e-4
    max_iters: int = 5000
    weight_decay: float = 1e-1
    beta1: float = 0.9
    beta2: float = 0.95
    grad_clip: float = 1.0
    decay_lr: bool = True
    warmup_iters: int = 500
    lr_decay_iters: int = 5000
    min_lr: float = 6e-5
    eval_interval: int = 200
    log_interval: int = 10
    eval_iters: int = 100
    checkpoint_dir: str = "ai_system/models/checkpoints"

class Config:
    """Central configuration management."""
    def __init__(self, model_cfg: Optional[ModelConfig] = None, train_cfg: Optional[TrainingConfig] = None):
        self.model = model_cfg or ModelConfig()
        self.training = train_cfg or TrainingConfig()

    def save(self, path: str):
        """Saves config to a YAML file."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = {
            "model": asdict(self.model),
            "training": asdict(self.training)
        }
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

    @classmethod
    def load(cls, path: str) -> "Config":
        """Loads config from a YAML file."""
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(
            model_cfg=ModelConfig(**data.get("model", {})),
            train_cfg=TrainingConfig(**data.get("training", {}))
        )

if __name__ == "__main__":
    # Example usage: Save default config
    cfg = Config()
    cfg.save("ai_system/app/config/default_config.yaml")
    print("Default configuration saved to ai_system/app/config/default_config.yaml")
