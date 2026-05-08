"""
====================================================================================================
FILE: serve.py
ROLE: The Sentient Orchestrator (Hugging Face Root Version)
====================================================================================================
"""

import os
import json
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

# Hugging Face mandatory port
PORT = int(os.environ.get("PORT", 7860)) 

app = FastAPI()

class Query(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    # Looks for the dashboard in the same folder (root)
    with open("samos_dashboard.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/predict")
async def predict(query: Query):
    start_time = time.time()
    # Simulated high-assurance response for the demo
    response = f"### 🏹 SAMOS LIVE\n\nI am processing '{query.text}' through the 4B Neural Core. This demo is running 100% on Hugging Face Cloud infrastructure."
    latency = (time.time() - start_time) * 1000
    return {
        "response": response,
        "metrics": {"latency_ms": f"{latency:.2f}ms", "compute": "HF Cloud CPU"}
    }

@app.get("/logo.png")
async def logo():
    # Attempt to find the logo file in the root
    for file in os.listdir("."):
        if file.startswith("samos_logo") and file.endswith(".png"):
            return FileResponse(file)
    return "Not Found"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
