FROM python:3.10-slim

# HuggingFace required env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create runtime dirs
RUN mkdir -p data logs sessions

# HuggingFace runs as root — DO NOT change user
# ❌ USER botuser (not allowed)

# Dummy web server so HF Space stays alive
CMD python -u main.py & python -m http.server ${PORT}
