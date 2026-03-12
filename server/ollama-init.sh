#!/bin/bash
# ==================================
# 🚀 Ollama Server Entrypoint
# ==================================
# This script initializes the Ollama server
# inside the container.
#
# It performs the following steps:
# 1️⃣ Start Ollama server in background
# 2️⃣ Wait for server to initialize
# 3️⃣ Pull Phi-3 Mini model if not already present
# 4️⃣ Keep container running
# ==================================

set -e  # Exit on errors

# ==================================
# 🎨 Colors for readable output
# ==================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

MODEL_DIR="/root/.ollama"
MODEL_NAME="phi3:mini"

echo -e "${YELLOW}🚀 Starting Ollama server...${NC}"

# Start Ollama server in background
ollama serve &

# Wait a few seconds for server to initialize
sleep 5

# ==================================
# 1️⃣ Ensure model directory exists
# ==================================

mkdir -p "$MODEL_DIR"

# ==================================
# 2️⃣ Pull Phi-3 Mini model if missing
# ==================================

if [ ! -d "$MODEL_DIR/$MODEL_NAME" ]; then
    echo -e "${YELLOW}📥 $MODEL_NAME model not found. Downloading...${NC}"
    ollama pull "$MODEL_NAME"
else
    echo -e "${GREEN}✅ $MODEL_NAME model already exists${NC}"
fi

# ==================================
# 3️⃣ Keep container running
# ==================================

echo -e "${GREEN}✅ Ollama server and model ready!${NC}"
echo -e "${YELLOW}⏳ Keeping container alive...${NC}"

# Wait indefinitely
tail -f /dev/null
