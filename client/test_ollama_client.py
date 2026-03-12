# test_ollama_client.py
import pytest
from unittest.mock import patch, MagicMock
from ollama_client import build_prompt, is_small_talk, stream_chat, SYSTEM_INSTRUCTION, MODEL

# ======================================
# Test build_prompt
# ======================================
def test_build_prompt_includes_system_instruction():
    prompt = "Explain Docker"
    result = build_prompt(prompt)
    assert SYSTEM_INSTRUCTION.strip() in result
    assert prompt in result
    assert "Answer:" in result

# ======================================
# Test small talk filter
# ======================================
def test_small_talk_detection():
    assert is_small_talk("hi")
    assert is_small_talk("hello there")
    assert not is_small_talk("Explain Docker in one sentence")
    assert not is_small_talk("How does Kubernetes work?")

# ======================================
# Test stream_chat with mocked requests
# ======================================
@patch("ollama_client.requests.post")
def test_stream_chat_mocked_success(mock_post):
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Docker is containerization."}
    mock_response.raise_for_status = lambda: None
    mock_post.return_value = mock_response

    # Run stream_chat
    result = stream_chat("Explain Docker")

    # Assertions
    assert "Docker is containerization." in result
    mock_post.assert_called_once()
    assert MODEL in mock_post.call_args[1]["json"]["model"]

@patch("ollama_client.requests.post")
def test_stream_chat_timeout(mock_post):
    # Simulate timeout exception
    mock_post.side_effect = Exception("Timeout error")
    result = stream_chat("Explain Docker")
    assert "⚠️ Error" in result

# ======================================
# Test Clipboard copy (if pyperclip available)
# ======================================
@patch("ollama_client.pyperclip.copy", autospec=True)
@patch("ollama_client.requests.post")
def test_stream_chat_clipboard(mock_post, mock_copy):
    try:
        import pyperclip
    except ModuleNotFoundError:
        pytest.skip("pyperclip not installed")

    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Test response"}
    mock_response.raise_for_status = lambda: None
    mock_post.return_value = mock_response

    stream_chat("Test prompt")
    mock_copy.assert_called_once_with("Test response")
