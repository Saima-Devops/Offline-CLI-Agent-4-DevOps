#!/bin/bash
# ==================================
# 🚀 Ollama Lightweight Stack Setup (Phi-3 Default)
# ==================================
# This script prepares the environment
# for the containerized Ollama AI stack with Phi-3 Mini.
#
# It performs the following steps:
# 1️⃣ Verify Docker installation
# 2️⃣ Verify Docker Compose
# 3️⃣ Check project files
# 4️⃣ Apply executable permissions
# 5️⃣ Create Docker model volume
# 6️⃣ Install global CLI command (ai)
# 7️⃣ Set default model to Phi-3 Mini
# 8️⃣ Build Docker images
# 9️⃣ Start Ollama server
#
# Run this script once after cloning
# the project.
# ==================================

set -e  # Exit immediately if a command fails

# ==================================
# 🎨 Colors for readable output
# ==================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ==================================
# 📁 Detect project directory
# ==================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

AI_SCRIPT="$SCRIPT_DIR/ai"
SERVER_SCRIPT="$SCRIPT_DIR/server/ollama-init.sh"

echo -e "${YELLOW}📁 Project directory:${NC} $SCRIPT_DIR"

# ==================================
# 1️⃣ Check Docker
# ==================================

echo -e "${YELLOW}🔍 Checking Docker installation...${NC}"

if ! command -v docker &> /dev/null
then
    echo -e "${RED}❌ Docker is not installed.${NC}"
    echo "Please install Docker and try again."
    exit 1
fi

# Check Docker daemon
if ! docker info &> /dev/null
then
    echo -e "${RED}❌ Docker daemon is not running.${NC}"
    echo "Please start Docker and try again."
    exit 1
fi

echo -e "${GREEN}✅ Docker detected${NC}"

# ==================================
# 2️⃣ Check Docker Compose
# ==================================

echo -e "${YELLOW}🔍 Checking Docker Compose...${NC}"

if ! docker compose version &> /dev/null
then
    echo -e "${RED}❌ Docker Compose not available.${NC}"
    echo "Please install Docker Compose."
    exit 1
fi

echo -e "${GREEN}✅ Docker Compose detected${NC}"

# ==================================
# 3️⃣ Validate Required Files
# ==================================

echo -e "${YELLOW}🔍 Checking required project files...${NC}"

if [ ! -f "$AI_SCRIPT" ]; then
    echo -e "${RED}❌ Error: ai script not found.${NC}"
    exit 1
fi

if [ ! -f "$SERVER_SCRIPT" ]; then
    echo -e "${RED}❌ Error: server/ollama-init.sh not found.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All required files found${NC}"

# ==================================
# 4️⃣ Apply Permissions
# ==================================

echo -e "${YELLOW}🔧 Applying executable permissions...${NC}"

chmod +x "$AI_SCRIPT"
chmod +x "$SERVER_SCRIPT"

echo -e "${GREEN}✅ Script permissions updated${NC}"

# ==================================
# 5️⃣ Create Docker Volume
# ==================================
# This volume stores downloaded models
# so they persist across container restarts

echo -e "${YELLOW}📦 Creating Docker model volume...${NC}"

docker volume inspect ollama-models >/dev/null 2>&1 || \
docker volume create ollama-models >/dev/null

echo -e "${GREEN}✅ Docker volume ready${NC}"

# ==================================
# 6️⃣ Install Global CLI Tool
# ==================================

echo -e "${YELLOW}⚙️ Installing global 'ai' CLI command...${NC}"

if [ -f /usr/local/bin/ai ]; then
    echo -e "${YELLOW}ℹ️ Existing ai command detected — updating...${NC}"
fi

sudo cp "$AI_SCRIPT" /usr/local/bin/ai
sudo chmod +x /usr/local/bin/ai

echo -e "${GREEN}✅ 'ai' command installed globally${NC}"

# ==================================
# 7️⃣ Set Default Model to Phi-3 Mini
# ==================================
# Ensures the CLI and containers use Phi-3 Mini by default

echo -e "${YELLOW}📝 Setting default model to Phi-3 Mini...${NC}"

export MODEL="phi3:mini"

# Update docker-compose.yml if MODEL exists
if grep -q "MODEL=" "$SCRIPT_DIR/docker-compose.yml"; then
    sed -i '' 's/MODEL=.*/MODEL=phi3:mini/' "$SCRIPT_DIR/docker-compose.yml"
fi

echo -e "${GREEN}✅ Default model set to phi3:mini${NC}"

# ==================================
# 8️⃣ Build Docker Images
# ==================================

echo -e "${YELLOW}🐳 Building Docker images...${NC}"

cd "$SCRIPT_DIR"
docker compose build

echo -e "${GREEN}✅ Docker images built successfully${NC}"

# ==================================
# 9️⃣ Start Ollama Server
# ==================================

echo -e "${YELLOW}🚀 Starting Ollama server container...${NC}"

docker compose up -d ollama

echo -e "${YELLOW}⏳ Waiting for server initialization...${NC}"
sleep 6

# Check container health
if docker ps | grep -q ollama
then
    echo -e "${GREEN}✅ Ollama server started${NC}"
else
    echo -e "${RED}❌ Failed to start Ollama container${NC}"
    exit 1
fi

# ==================================
# 🎉 Setup Complete
# ==================================

echo ""
echo -e "${GREEN}🎉 Ollama Lightweight Stack (Phi-3 Mini) is ready!${NC}"
echo ""
echo "You can now run AI prompts from anywhere:"
echo ""
echo "   ai \"Explain Docker in one sentence\""
echo ""
echo "Or start interactive mode:"
echo ""
echo "   ai"
echo ""
echo "🌐 Ollama API endpoint:"
echo "   http://localhost:11434"
echo ""
echo "✅ Default model in use: phi3:mini"
echo ""
