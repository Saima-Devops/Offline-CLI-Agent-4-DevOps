# 🤖 Offline CLI Agent for DevOps Users & Developers

A **lightweight offline AI CLI assistant** designed for **DevOps engineers**.
This project runs a local large language model using **Ollama** and the **Phi‑3 Mini model** inside **Docker**, allowing users to interact with an **AI assistant** without relying on **external cloud APIs**.

The assistant runs in the terminal and helps answer **DevOps, cloud, Linux,** and **infrastructure questions**.

<br>

**⭐ Runs fully offline — your AI assistant stays private and secure.**

---

## 📌 Project Goals

This project demonstrates how to build a **secure, lightweight, offline AI assistant** with:

- Local LLM execution

- Containerized architecture

- CI/CD automation

- Security scanning

- CLI-based interaction

> It is designed as a portfolio-ready DevOps + AI integration project.

-----

## 🏗 Architecture Overview

User Terminal <br>
      │<br>
      ▼ <br>
Python CLI Client <br>
     │ <br>
     ▼ <br>
Ollama API (Docker Container) <br>
     │ <br>
     ▼ <br>
Phi-3 Mini Local Model <br>
 
---

## Components:

- Ollama Phi-3 Mini Local Model
- Python Scripts for main logic
- Shell Scripts for automation
- Docker & Docker Compose for containerization 
- Dockerfile
- docker-compose.yml

----

## ⚙️ Features

✅ Offline **AI assistant** <br>
✅ DevOps-focused responses <br>
✅ Runs completely inside Docker <br>
✅ Lightweight model (Phi-3 Mini) <br>
✅ CLI interface with emoji prompts <br>
✅ Small-talk filter for irrelevant prompts <br>
✅ AI thinking animation in the terminal <br>
✅ Response time tracking <br>
✅ Health-checked containers <br>
✅ CI pipeline with automated tests <br>
✅ Docker image is published automatically after the **CI pipeline** is activated.

----

## 🧠 AI Model

This project uses: **Phi‑3 Mini**

### Advantages:

- Small footprint (~2GB)

- Fast inference

- Works on laptops/small machines 

- Runs offline

- Ideal for developers and DevOps engineers who are used to work on CLI with limited internet access

----

## 📦 Docker Hub Image

The prebuilt container image is available on:

**Docker Hub Repository**

```bash
saim2026/ollama-agent:v1.01
```

**Users can pull and run the image directly without building the project.**

---

## 🚀 Quick Start (Run From Docker Hub) - Option#1

### 1️⃣ Install prerequisites

Make sure you have:

- Docker installed

- Docker Compose installed

**Verify installation:**

```bash
docker --version
docker compose version
```

---

### 📥 Step 1 — Pull the Docker Image

```bash
docker pull saim2026/ollama-agent:v1.01
```

---

### 📂 Step 2 — Create a docker-compose.yml

Create a file named: `docker-compose.yml` or download from the repo

Paste the following configuration:

```bash
version: "3.9"

services:

  ollama:
    image: ollama/ollama
    container_name: ollama-server
    ports:
      - "11434:11434"

    volumes:
      - ollama-models:/root/.ollama

    restart: unless-stopped

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      retries: 5
      start_period: 40s

  client:
    image: saim2026/ollama-agent:v1.01
    container_name: ollama-client

    depends_on:
      ollama:
        condition: service_healthy

    environment:
      - OLLAMA_URL=http://ollama:11434
      - MODEL=phi3:mini

    stdin_open: true
    tty: true

volumes:
  ollama-models:
```
----

### ▶️ Step 3 — Start the AI Assistant

Run:
```bash
docker compose up
```

**Docker will:**

1. Start the Ollama server
2. Download the Phi-3 Mini model
3. Launch the CLI AI client

-----

### 💬 Example Usage

```bash
👤 YOU: explain Kubernetes in one line

🤖 AI:
Kubernetes is a container orchestration system.

• Manages container deployments
• Handles scaling automatically
• Provides service discovery
• Enables self-healing infrastructure
```
-----

## Option#2 - Download the entire project from the GitHub repo

STEP 1️⃣: mkdir && cd into the root folder

STEP 2️⃣: Make Sure Scripts Are Executable

Check both your scripts:

```bash
chmod +x setup.sh
chmod +x ollama-server/ollama-init.sh
chmod +x ai
```

STEP 3️⃣: Run Setup Script

Run your setup.sh:

```bash
./setup.sh
```

**What it does:**

- Checks Docker & Docker Compose.

- Validates project files (ai and ollama-init.sh).

- Applies executable permissions.

- Creates Docker volume ollama-models.

- Installs the global ai command (/usr/local/bin/ai).

- Sets default model to Phi-3 Mini.

- Builds Docker images (docker compose build).

- Starts the Ollama server container (docker compose up -d ollama).

✅ After this, you should see:

```bash
🎉 Ollama Lightweight Stack (Phi-3 Mini) is ready!
You can now run AI prompts from anywhere:
   ai "Explain Docker in one sentence"
```

**After that you can simply run:**

```bash
ai "Explain Docker in one sentence"
```

or access the ai CLI prompt globally from anywhere

```bash
ai
```

### ✅ Notes

- No need to pull `Phi-3` manually — ollama-init.sh handles it.

- Global CLI `ai` works anywhere (/usr/local/bin/ai).

- Docker volume `ollama-models` persists downloaded models across restarts.

- Your `setup.sh` automates everything from permissions to server start.

-----

### 📁 Project Structure
```bash
ollama-stack/
│
├── client/
│   ├── ollama_client.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── server/
│   └── ollama-init.sh
│
├── tests/
│   └── test_ollama_client.py
│
├── docker-compose.yml
│
└── .github/workflows/
    ├── ci.yml
    └── cd.yml
```
------

### 🔄 CI/CD Pipeline

CI/CD is implemented using GitHub Actions.

**Pipeline stages:**

#### CI Pipeline

1️⃣ Code checkout <br>
2️⃣ Install Python dependencies <br>
3️⃣ Run automated tests (pytest) <br>
4️⃣ Validate Docker build <br>

#### CD Pipeline

1️⃣ Build Docker image <br>
2️⃣ Security scan <br>
3️⃣ Push image to Docker Hub <br>

-----

### 🔒 Security Practices

This project includes security-focused DevOps practices:

- Container isolation

- Minimal base images

- Health checks

- Automated CI testing

- Docker image versioning

- Dependency management

<br>

**Optional improvements:**

- Container vulnerability scanning

- SAST scanning

- SBOM generation

-----

### 🧪 Testing

**Run tests locally:**

```bash
pytest
```

**Tests validate:**

- Prompt generation

- Small talk filtering

- API request logic

- CLI functionality

------

### 🛠 Future Improvements

- Conversation memory

- Streaming responses

- DevOps command generation

- Kubernetes deployment

- GPU acceleration

- Web UI dashboard

-----

### 👩‍💻 Author

Developed by:

**Saima Usman**
DevOps & Cloud Enthusiast

<br>

### ⭐ Support

**If you find this project useful:**

- Star the repository

- Share with DevOps community

- Open Issues for improvements


-----

