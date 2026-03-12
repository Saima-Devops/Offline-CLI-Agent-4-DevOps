#!/usr/bin/env python3
import requests
import sys
import os
from datetime import datetime
import json
import threading
import time

# Optional clipboard support
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ModuleNotFoundError:
    CLIPBOARD_AVAILABLE = False

# ======================================
# Configuration
# ======================================
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "phi3:mini")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))

# ======================================
# Small talk filter
# ======================================
SMALL_TALK = [
    "hi", "hello", "ok", "hey", "thanks", "thank you",
    "sorry", "how are you", "how are you?", "good morning",
    "good night", "good afternoon", "good evening", "shut up",
    "i love you",
]

# ======================================
# System Instruction
# ======================================
SYSTEM_INSTRUCTION = """
You are a professional AI assistant.

Rules:
1. Provide clear and structured answers.
2. Start with one summary sentence.
3. Then provide 3-5 bullet points.
4. Keep answers concise.
"""

# ======================================
# Dots animation for "AI thinking"
# ======================================
def thinking_dots(stop_event):
    print("🤖 AI is thinking", end="", flush=True)
    dot_count = 0
    while not stop_event.is_set():
        print(".", end="", flush=True)
        dot_count += 1
        if dot_count >= 3:
            print("\b\b\b   \b\b\b", end="", flush=True)  # erase dots
            dot_count = 0
        time.sleep(0.5)
    print("\n", end="", flush=True)

# ======================================
# Build prompt
# ======================================
def build_prompt(user_prompt):
    return f"""
{SYSTEM_INSTRUCTION}

User Question:
{user_prompt}

Answer:
"""

# ======================================
# Check if user prompt is small talk
# ======================================
def is_small_talk(prompt):
    p = prompt.lower()
    for word in SMALL_TALK:
        if p == word or p.startswith(word):
            return True
    return False

# ======================================
# Chat with AI
# ======================================
def stream_chat(prompt):
    stop_event = threading.Event()
    thread = threading.Thread(target=thinking_dots, args=(stop_event,))
    thread.start()

    full_response = ""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": build_prompt(prompt),
                "stream": False,
                "options": {"temperature": 0.3, "top_p": 0.9, "num_predict": 512}
            },
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        full_response = data.get("response", "").strip()

        stop_event.set()
        thread.join()

        print("🤖 AI:\n")
        print(full_response)

        if CLIPBOARD_AVAILABLE and full_response:
            pyperclip.copy(full_response)
            print("📋 Response copied to clipboard!\n")

        return full_response

    except requests.exceptions.Timeout:
        stop_event.set()
        thread.join()
        return "\n⚠️ Error: Model response timeout.\n"

    except requests.exceptions.ConnectionError:
        stop_event.set()
        thread.join()
        return "\n⚠️ Error: Cannot connect to Ollama. Is Docker running?\n"

    except KeyboardInterrupt:
        stop_event.set()
        thread.join()
        print("\n👋 Interrupted by user.\n")
        return ""

    except Exception as e:
        stop_event.set()
        thread.join()
        return f"\n⚠️ Error: {str(e)}\n"

# ======================================
# CLI Header
# ======================================
def print_header():
    print("="*70)
    print("🚀 LIGHTWEIGHT OLLAMA AI CLIENT")
    print(f"🧠 Model: {MODEL}")
    print(f"🌐 Endpoint: {OLLAMA_URL}")
    print("💬 Please ask technical or DevOps related questions")
    print("="*70)

# ======================================
# Main CLI Logic
# ======================================
def main():
    print_header()

    # Single prompt mode
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(f"\n👤 YOU: {prompt}")

        if is_small_talk(prompt):
            print("\n⚠️ Please ask a relevant question.\n")
            return

        start = datetime.now()
        response = stream_chat(prompt)
        duration = (datetime.now() - start).total_seconds()
        print(f"⏱ Response Time: {duration:.2f}s\n")

    # Interactive mode
    else:
        print("\n💬 Interactive Mode (type 'quit' to exit)\n")
        while True:
            try:
                prompt = input("👤 YOU: ").strip()
                if prompt.lower() in ["quit", "exit", "q"]:
                    print("\n👋 Goodbye!\n")
                    break
                if not prompt:
                    continue
                if is_small_talk(prompt):
                    print("\n⚠️ Please ask a relevant question.\n")
                    continue

                start = datetime.now()
                response = stream_chat(prompt)
                duration = (datetime.now() - start).total_seconds()
                print(f"⏱ Response Time: {duration:.2f}s\n")

            except KeyboardInterrupt:
                print("\n👋 Interrupted. Exiting client.\n")
                break

# ======================================
# Program Entry Point
# ======================================
if __name__ == "__main__":
    main()
