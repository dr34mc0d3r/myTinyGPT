import os
import re
from typing import List, Dict, Any

def clean_markdown(text: str) -> str:
    """
    Cleans markdown text by removing heavy formatting like image links or complex HTML,
    making it more suitable for LLM context processing.
    """
    # Remove image links
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove raw links
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # Remove markdown headers
    text = re.sub(r'#+\s', '', text)
    # Remove code block markers
    text = re.sub(r'```[a-z]*', '', text)
    # Basic whitespace cleanup
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def load_markdown_files(directory: str) -> List[Dict[str, Any]]:
    """
    Recursively loads all .md files from a directory and its subdirectories,
    cleans them, and returns them as a list of dicts.
    """
    documents = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()
                        cleaned_content = clean_markdown(content)
                        documents.append({
                            "id": filepath, # Using full path as id for uniqueness
                            "content": cleaned_content,
                            "metadata": {"source": filepath}
                        })
                    except Exception as e:
                        print(f"Skipping file {filepath} due to error: {e}")
    return documents
