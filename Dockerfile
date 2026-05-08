# 🐳 SAMOS: Hugging Face Optimized Dockerfile

FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app

# [PHASE 24] Security
RUN groupadd -r samos && useradd -r -g samos samos

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src/ ./src/
COPY models/ ./models/
COPY samos_dashboard.html .
COPY samos_logo_ai_*.png . 

RUN chown -R samos:samos /app
USER samos

# 🛡️ HUGGING FACE COMPLIANCE: EXPOSE 7860
EXPOSE 7860

ENV PYTHONPATH="."
# Ensure the port is passed to the script
ENV PORT=7860

# Launch the engine
CMD ["python", "src/sre/serve.py"]
