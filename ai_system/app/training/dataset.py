import os
import torch
from torch.utils.data import Dataset, DataLoader
from typing import List, Tuple
from app.tokenizer.processor import TokenizerProcessor

class TextDataset(Dataset):
    """
    Simple dataset that loads text files and chunks them into tokenized sequences.
    """
    def __init__(self, data_path: str, tokenizer: TokenizerProcessor, block_size: int):
        self.tokenizer = tokenizer
        self.block_size = block_size
        
        # Load and tokenize the entire dataset
        # For very large datasets, we would use a memory-mapped approach
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found at {data_path}")
            
        with open(data_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        print(f"Tokenizing {len(text)} characters of text...")
        self.tokens = torch.tensor(self.tokenizer.encode(text), dtype=torch.long)
        print(f"Total tokens in dataset: {len(self.tokens)}")

    def __len__(self):
        # We subtract block_size to ensure we can always get a full window
        return len(self.tokens) - self.block_size

    def __getitem__(self, idx) -> Tuple[torch.Tensor, torch.Tensor]:
        # idx is the start of the window
        # chunk is block_size tokens for input (x)
        # target is block_size tokens for target (y), shifted by 1
        x = self.tokens[idx : idx + self.block_size]
        y = self.tokens[idx + 1 : idx + self.block_size + 1]
        return x, y

def create_dataloader(data_path: str, tokenizer: TokenizerProcessor, block_size: int, batch_size: int, shuffle: bool = True):
    dataset = TextDataset(data_path, tokenizer, block_size)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, pin_memory=True)

if __name__ == "__main__":
    # Test dataset
    from app.config.config import ModelConfig
    
    tokenizer_model = "models/tokenizer/tokenizer.model"
    if not os.path.exists(tokenizer_model):
         tokenizer_model = "../../models/tokenizer/tokenizer.model"
         
    tokenizer = TokenizerProcessor(tokenizer_model)
    config = ModelConfig()
    
    sample_data = "data/raw/sample_corpus.txt"
    if not os.path.exists(sample_data):
        sample_data = "../../data/raw/sample_corpus.txt"
        
    dataset = TextDataset(sample_data, tokenizer, config.block_size)
    x, y = dataset[0]
    print(f"Input shape: {x.shape}, Target shape: {y.shape}")
    print(f"First 10 tokens x: {x[:10]}")
    print(f"First 10 tokens y: {y[:10]}")
