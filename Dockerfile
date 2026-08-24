FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "blackbird.py"]
