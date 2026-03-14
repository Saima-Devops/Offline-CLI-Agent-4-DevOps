FROM ollama/ollama:latest

WORKDIR /app

# Install Python + curl
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl

# Copy files
COPY ollama_client.py .
COPY requirements.txt .
COPY ollama-init.sh /

# Install python packages
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Make init script executable
RUN chmod +x /ollama-init.sh

ENTRYPOINT ["/ollama-init.sh"]
