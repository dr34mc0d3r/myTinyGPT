import os
import sentencepiece as spm
from typing import List, Union

class TokenizerProcessor:
    """
    Handles loading, encoding, and decoding using a trained SentencePiece model.
    """
    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Tokenizer model not found at {model_path}")
        
        self.sp = spm.SentencePieceProcessor()
        self.sp.load(model_path)
        
    @property
    def vocab_size(self) -> int:
        return self.sp.get_piece_size()
    
    @property
    def pad_id(self) -> int:
        return self.sp.pad_id()
    
    @property
    def unk_id(self) -> int:
        return self.sp.unk_id()
    
    @property
    def bos_id(self) -> int:
        return self.sp.bos_id()
    
    @property
    def eos_id(self) -> int:
        return self.sp.eos_id()

    def encode(self, text: str, add_bos: bool = False, add_eos: bool = False) -> List[int]:
        """
        Encodes text into a list of token IDs.
        """
        ids = self.sp.encode_as_ids(text)
        if add_bos:
            ids = [self.bos_id] + ids
        if add_eos:
            ids = ids + [self.eos_id]
        return ids

    def decode(self, ids: List[int]) -> str:
        """
        Decodes a list of token IDs back into text.
        """
        return self.sp.decode_ids(ids)

    def token_to_id(self, token: str) -> int:
        return self.sp.piece_to_id(token)

    def id_to_token(self, token_id: int) -> str:
        return self.sp.id_to_piece(token_id)

if __name__ == "__main__":
    # Example usage for testing
    model_path = "models/tokenizer/tokenizer.model"
    if not os.path.exists(model_path):
        # If run from tokenizer dir
        model_path = "../../models/tokenizer/tokenizer.model"
    
    if os.path.exists(model_path):
        processor = TokenizerProcessor(model_path)
        text = "AI engineering is fun!"
        encoded = processor.encode(text, add_bos=True, add_eos=True)
        decoded = processor.decode(encoded)
        
        print(f"Original: {text}")
        print(f"Encoded:  {encoded}")
        print(f"Decoded:  {decoded}")
        print(f"Vocab size: {processor.vocab_size}")
    else:
        print("Model not found. Run trainer.py first.")
