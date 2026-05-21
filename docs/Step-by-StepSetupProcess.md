# myTinyGPT: Step-by-Step Setup & Lifecycle Guide

This document provides a definitive guide for setting up `myTinyGPT` and managing its lifecycle, including a "fresh start" procedure.

---

## 1. Corrected Setup Process

Follow these steps in order to get the system operational.

| Step | Command | Purpose |
| :--- | :--- | :--- |
| **1** | Populate `ai_system/data/raw/` | Add your source Markdown files (e.g., MDN docs) for the knowledge base. |
| **2** | `python3 ai_system/scripts/index_js_docs.py` | Index documents into the Hybrid Retrieval system (ChromaDB). |
| **3** | `python3 -m ai_system.app.training.trainer` | Train the Tiny Transformer on your corpus. |
| **4** | `python3 -m ai_system.app.api.main` | Start the FastAPI inference server for chat. |
| **5 (Opt)** | `python3 ai_system/data/chroma_browser.py` | Inspect the indexed knowledge base vectors. |

---

## 2. Generated File Artifacts

Each step produces specific files that are critical to the system's state.

### Step 2: Indexing Artifacts
- `ai_system/data/embeddings/chroma/chroma.sqlite3`: The metadata database.
- `ai_system/data/embeddings/chroma/[UUID]/`: Binary index files (`data_level0.bin`, `link_lists.bin`, etc.).

### Step 3: Training Artifacts
- `ai_system/models/checkpoints/ckpt_best.pt`: The trained weights and configuration.
- `ai_system/logs/events.out.tfevents.[timestamp]`: TensorBoard metrics for loss and learning rate.

### Step 4: API/Chat Artifacts
- **Memory Updates:** The system may update `ai_system/data/embeddings/chroma/` to store conversation history in the `mytinygpt_memory` collection.

---

## 3. Fresh Start (Reset) Procedure

To completely reset the system and clear all data, models, and history, follow these steps. **Warning:** This cannot be undone.

### Files to Delete:
1.  **Knowledge Base & Memory:** `ai_system/data/embeddings/chroma`
2.  **Trained Model:** `ai_system/models/checkpoints/ckpt_best.pt`
3.  **Training Logs:** `ai_system/logs/events.out.tfevents.*`
4.  **Indexing Logs:** `ai_system/logs/indexing_*.log`

### Reset Commands:
```bash
# Reset Database and Memory
rm -rf ai_system/data/embeddings/chroma

# Reset Trained Models
rm -f ai_system/models/checkpoints/ckpt_best.pt

# Reset Logs
rm -f ai_system/logs/*.log
rm -f ai_system/logs/events.out.tfevents.*
```

*After running these commands, you can begin again at Step 1.*
