FROM python:3.11-slim

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY uv.lock .

RUN pip install --no-cache-dir uv && \
    uv sync

COPY . .

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app \
    && chmod +x /app/start.sh

USER appuser

EXPOSE 8080

ENTRYPOINT ["./start.sh"]
