# ARTPARK MCP Server - Production Dockerfile
# Adapted from esankhyiki-mcp
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OTEL_SERVICE_NAME=artpark-mcp-server
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap -a install

COPY artpark_server.py .
COPY artpark/ ./artpark/
COPY observability/ ./observability/
COPY publicdata/data/ ./publicdata/data/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["opentelemetry-instrument", "fastmcp", "run", "artpark_server.py:mcp", "--transport", "http", "--port", "8000", "--host", "0.0.0.0"]
