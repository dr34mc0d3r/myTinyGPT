import os
import sentencepiece as spm
from typing import List, Optional

class TokenizerTrainer:
    """
    Handles training of the SentencePiece tokenizer.
    """
    def __init__(
        self,
        vocab_size: int = 8000,
        model_type: str = "unigram",
        model_prefix: str = "tokenizer",
        character_coverage: float = 1.0,
        pad_id: int = 0,
        unk_id: int = 1,
        bos_id: int = 2,
        eos_id: int = 3,
    ):
        self.vocab_size = vocab_size
        self.model_type = model_type
        self.model_prefix = model_prefix
        self.character_coverage = character_coverage
        self.pad_id = pad_id
        self.unk_id = unk_id
        self.bos_id = bos_id
        self.eos_id = eos_id

    def train(self, input_files: List[str], output_dir: str):
        """
        Trains the SentencePiece model.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        model_path_prefix = os.path.join(output_dir, self.model_prefix)
        
        # Define training arguments
        # We use a comma-separated string for input files as required by spm_train
        input_arg = ",".join(input_files)
        
        train_args = (
            f"--input={input_arg} "
            f"--model_prefix={model_path_prefix} "
            f"--vocab_size={self.vocab_size} "
            f"--model_type={self.model_type} "
            f"--character_coverage={self.character_coverage} "
            f"--pad_id={self.pad_id} "
            f"--unk_id={self.unk_id} "
            f"--bos_id={self.bos_id} "
            f"--eos_id={self.eos_id} "
            f"--pad_piece=[PAD] "
            f"--unk_piece=[UNK] "
            f"--bos_piece=[BOS] "
            f"--eos_piece=[EOS] "
            f"--user_defined_symbols=[SEP],[MASK]"
        )

        print(f"Starting SentencePiece training with vocab_size={self.vocab_size}...")
        spm.SentencePieceTrainer.train(train_args)
        print(f"Tokenizer training complete. Files saved to {output_dir}")

if __name__ == "__main__":
    # Example usage for testing
    import sys
    
    # Path to sample corpus
    input_corpus = "data/raw/sample_corpus.txt"
    if not os.path.exists(input_corpus):
        # If run from tokenizer dir
        input_corpus = "../../data/raw/sample_corpus.txt"
        
    trainer = TokenizerTrainer(vocab_size=100) # Small vocab for testing with small corpus
    trainer.train([input_corpus], "models/tokenizer")
