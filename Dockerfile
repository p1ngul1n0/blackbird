FROM python:3.12-slim

# Install system dependencies and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install setuptools
RUN python3 -m pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN python3 -m pip install -r requirements.txt

# Copy the rest of the application
COPY . .

ENTRYPOINT ["python3","blackbird.py"]