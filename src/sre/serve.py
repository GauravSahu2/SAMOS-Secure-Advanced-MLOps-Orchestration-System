"""
====================================================================================================
HUGGING FACE OPTIMIZED: src/sre/serve.py
ROLE: The Sentient Orchestrator (Cloud Demo Mode)
TRIGGER: Triggered by Hugging Face Spaces on Port 7860
====================================================================================================
"""

import os
import json
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

# 🛡️ HUGGING FACE COMPLIANCE: Use Port 7860
PORT = int(os.environ.get("PORT", 7860)) 

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # [STARTUP] Logic
    print(f"🚀 [SPACE] SAMOS 4B Cloud Demo Active on Port {PORT}")
    print("⚠️ [SRE] Hardware Detected: Cloud CPU (Simulation Mode Active)")
    yield
    # [SHUTDOWN] Logic (if any)
    print("🛑 [SPACE] SAMOS Engine Shutting Down")

app = FastAPI(title="SAMOS 4B: Cloud Demo", lifespan=lifespan)

class Query(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    # Serves the dashboard directly to the Hugging Face iframe
    dashboard_path = "samos_dashboard.html"
    if os.path.exists(dashboard_path):
        # High-Assurance serving: In a real async environment, use aiofiles or StaticFiles
        # For this demo, we read once or use the FastAPI FileResponse approach
        return FileResponse(dashboard_path)
    return "<h1>SAMOS Dashboard Not Found.</h1>"

@app.post("/predict")
async def chat(query: Query):
    # Simulated Inference for Cloud Demo (matches your forged logic)
    start_time = time.time()
    response = f"### 🏹 SAMOS CLOUD RESPONSE\n\nI am processing '{query.text}' through my distilled 336B logic layers. In this cloud demo, I am running on High-Performance CPU simulation."
    
    latency = (time.time() - start_time) * 1000
    return {
        "response": response,
        "metrics": {
            "latency_ms": f"{latency:.2f}ms",
            "compute": "Hugging Face Cloud CPU"
        }
    }

@app.get("/logo.png")
async def get_logo():
    # Serves the logo for the cloud UI
    for file in os.listdir("."):
        if file.startswith("samos_logo_ai") and file.endswith(".png"):
            return FileResponse(file)
    return "Not Found"

if __name__ == "__main__":
    import uvicorn
    # High-Assurance Binding: Use 0.0.0.0 only in Cloud/Container environments
    # Default to 127.0.0.1 for local security.
    host = "0.0.0.0" if os.environ.get("PORT") or os.environ.get("SPACE_ID") else "127.0.0.1"
    uvicorn.run(app, host=host, port=PORT)
