FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ollama_client.py .

CMD ["python", "ollama_client.py"]
