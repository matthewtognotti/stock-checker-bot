# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

WORKDIR /app

# --- Builder stage ---
FROM base AS builder

# Install Chrome/Chromedriver in builder stage
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        fonts-liberation \
        wget \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

RUN python -m venv /app/.venv

COPY --link requirements.txt ./

ENV PIP_CACHE_DIR=/root/.cache/pip
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install -r requirements.txt

COPY --link . .

# --- Final stage ---
FROM base AS final

# Install Chrome/Chromedriver again in final stage
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        fonts-liberation \
        && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser
USER appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

CMD ["python", "main.py"]
