import pytest
from unittest.mock import patch, MagicMock
import requests

from ollama_client import build_prompt, is_small_talk, stream_chat


# ===============================
# Test: Prompt Builder
# ===============================
def test_build_prompt():
    prompt = "What is Docker?"
    result = build_prompt(prompt)

    assert "User Question" in result
    assert prompt in result
    assert "Answer:" in result


# ===============================
# Test: Small Talk Detection
# ===============================
def test_small_talk_detection():
    assert is_small_talk("hi") is True
    assert is_small_talk("hello there") is True
    assert is_small_talk("good morning") is True
    assert is_small_talk("explain kubernetes") is False


# ===============================
# Test: Successful AI Response
# ===============================
@patch("ollama_client.requests.post")
def test_stream_chat_mocked_success(mock_post):

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": "Docker is containerization."
    }
    mock_response.raise_for_status = lambda: None

    mock_post.return_value = mock_response

    response = stream_chat("Explain Docker")

    assert "Docker is containerization." in response


# ===============================
# Test: Timeout Handling
# ===============================
@patch("ollama_client.requests.post")
def test_stream_chat_timeout(mock_post):

    mock_post.side_effect = requests.exceptions.Timeout

    response = stream_chat("Explain Kubernetes")

    assert "timeout" in response.lower()


# ===============================
# Test: Connection Error Handling
# ===============================
@patch("ollama_client.requests.post")
def test_stream_chat_connection_error(mock_post):

    mock_post.side_effect = requests.exceptions.ConnectionError

    response = stream_chat("Explain DevOps")

    assert "cannot connect" in response.lower()
