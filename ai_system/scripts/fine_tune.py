import os
import torch
import sys

# Add the ai_system directory to sys.path to ensure imports work correctly
# regardless of where the script is executed from.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from app.training.trainer import Trainer
from app.config.config import Config

def fine_tune():
    """
    Fine-tunes the model on instruction data to improve agentic behavior (THINK/RESPOND format).
    """
    print("--- Starting Instruction Fine-Tuning ---")
    
    # 1. Load base configuration
    config = Config()
    
    # 2. Adjust for fine-tuning
    # We use a lower learning rate and fewer iterations for fine-tuning to avoid catastrophic forgetting.
    config.training.learning_rate = 1e-4
    config.training.max_iters = 100 
    config.training.eval_interval = 20
    config.training.log_interval = 5
    config.training.batch_size = 4
    config.training.checkpoint_dir = "ai_system/models/checkpoints"
    
    # 3. Initialize Trainer
    # Note: Trainer will initialize a fresh model and optimizer.
    trainer = Trainer(config)
    
    # 4. Load the best pre-trained checkpoint weights
    checkpoint_path = "ai_system/models/checkpoints/ckpt_best.pt"
    if os.path.exists(checkpoint_path):
        print(f"Loading weights from {checkpoint_path}...")
        # weights_only=False is required for loading checkpoints that contain custom objects (Config).
        checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
        trainer.model.load_state_dict(checkpoint['model'])
        print("Pre-trained weights successfully loaded.")
    else:
        print(f"Warning: {checkpoint_path} not found. Fine-tuning from a randomly initialized model.")

    # 5. Define instruction data path
    train_data = "ai_system/data/raw/instruction_data.txt"
    if not os.path.exists(train_data):
        print(f"Error: Instruction data not found at {train_data}")
        return

    # 6. Run fine-tuning
    print(f"Fine-tuning on {train_data} for {config.training.max_iters} iterations...")
    trainer.train(train_data)
    
    # 7. Save final fine-tuned model
    # We save it with a specific tag to distinguish it from the base model.
    trainer.save_checkpoint(config.training.max_iters, 0.0, tag="fine_tuned")
    print("--- Fine-Tuning Complete ---")
    print("The model is now trained on the THINK/RESPOND format.")
    print("Fine-tuned checkpoint saved as: ai_system/models/checkpoints/ckpt_fine_tuned.pt")

if __name__ == "__main__":
    fine_tune()
