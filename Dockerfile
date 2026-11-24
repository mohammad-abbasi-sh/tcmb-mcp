# tcmb-mcp — minimal image for MCP hosts and directory checks (e.g. Glama).
# Stdio server; no secrets needed. Glama builds this image and probes
# MCP initialize + tools/list with nothing configured.
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN pip install --no-cache-dir tcmb-mcp
CMD ["tcmb-mcp"]
