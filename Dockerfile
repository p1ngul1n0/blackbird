FROM python:3.12-slim

COPY . .

RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3","blackbird.py"]