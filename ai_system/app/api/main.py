import os
import time
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
import structlog

from ai_system.app.llm.inference import Generator
from ai_system.app.retrieval.manager import RetrievalManager
from ai_system.app.tools.registry import ToolRegistry
from ai_system.app.tools.calculator import CalculatorTool
from ai_system.app.agent.controller import AgentController
from ai_system.app.memory.manager import MemoryManager

# Setup logging
logger = structlog.get_logger()

# Initialize components (singleton-like for the app)
# In a real app, these would be managed via dependency injection
CHROME_PERSIST_DIR = "ai_system/data/embeddings/chroma"
MODEL_CHECKPOINT = "ai_system/models/checkpoints/ckpt_best.pt"
TOKENIZER_MODEL = "ai_system/models/tokenizer/tokenizer.model"

# Global state for components
app_state = {}

def get_agent_controller():
    if "agent" not in app_state:
        if not os.path.exists(MODEL_CHECKPOINT):
            raise RuntimeError(f"Model checkpoint not found at {MODEL_CHECKPOINT}. Run training first.")
        
        logger.info("api_startup", message="Initializing Agent components...")
        generator = Generator(MODEL_CHECKPOINT, TOKENIZER_MODEL)
        retrieval_manager = RetrievalManager(persist_directory=CHROME_PERSIST_DIR)
        tool_registry = ToolRegistry()
        tool_registry.register(CalculatorTool())
        memory_manager = MemoryManager()
        
        app_state["agent"] = AgentController(
            generator, 
            retrieval_manager, 
            tool_registry, 
            memory_manager
        )
        app_state["retrieval"] = retrieval_manager
        logger.info("api_startup", message="Agent components initialized.")
    return app_state["agent"]

# FastAPI App
app = FastAPI(
    title="myTinyGPT API",
    description="Local AI Inference Server with Agentic Hybrid Retrieval",
    version="0.1.0"
)

# Models
class ChatRequest(BaseModel):
    query: str
    max_iterations: Optional[int] = 1

class ChatResponse(BaseModel):
    query: str
    response: str
    time_taken_ms: float

class RetrievalRequest(BaseModel):
    query: str
    k: Optional[int] = 5

class RetrievalResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]

# Endpoints
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        agent = get_agent_controller()
        start_time = time.time()
        
        response = agent.run(request.query, max_iterations=request.max_iterations)
        
        end_time = time.time()
        return ChatResponse(
            query=request.query,
            response=response,
            time_taken_ms=(end_time - start_time) * 1000
        )
    except Exception as e:
        logger.error("api_error", endpoint="/chat", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrieve", response_model=RetrievalResponse)
async def retrieve(request: RetrievalRequest):
    try:
        # Ensure agent components are initialized
        get_agent_controller()
        retrieval_manager = app_state["retrieval"]
        
        results = retrieval_manager.retrieve(request.query, k=request.k)
        return RetrievalResponse(
            query=request.query,
            results=results
        )
    except Exception as e:
        logger.error("api_error", endpoint="/retrieve", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
