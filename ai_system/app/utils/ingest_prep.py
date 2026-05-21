"""
Utility: ingest_prep.py
Purpose: Provides pre-indexing cleanup and preparation tasks for the data directory.

WHAT:
This utility contains functions to prepare raw data before it is processed by the 
markdown parser and retrieval manager.

HOW:
1. `clean_hidden_files(directory)`: Recursively walks the directory tree to identify 
   and delete hidden files (e.g., those starting with '.' or '._').
2. This ensures that the main ingestion pipeline only encounters valid files,
   preventing encoding errors or unnecessary indexing of system artifacts.
"""

import os
import shutil

def clean_hidden_files(directory: str):
    """
    Recursively deletes hidden system files (starting with '.' or '._') 
    from the specified directory.
    """
    print(f"Cleaning hidden system files from: {directory}")
    files_deleted = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.startswith(".") or filename.startswith("._"):
                filepath = os.path.join(root, filename)
                try:
                    os.remove(filepath)
                    print(f"Deleted hidden file: {filepath}")
                    files_deleted += 1
                except Exception as e:
                    print(f"Error deleting {filepath}: {e}")
    print(f"Cleanup complete. Removed {files_deleted} files.")
