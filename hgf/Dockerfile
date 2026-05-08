# 🐳 SAMOS 4B: Cloud-Foolproof Dockerfile
# Strategy: Flat-Root Deployment

FROM python:3.12-slim
WORKDIR /app

# Install only essential tools for a fast launch
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy EVERYTHING from the root into /app
COPY . .

# Hugging Face Compliance
EXPOSE 7860
ENV PORT=7860

# Trigger the sentient engine (now in root)
CMD ["python", "serve.py"]
