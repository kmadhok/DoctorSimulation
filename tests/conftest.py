import pytest
import os
from unittest.mock import MagicMock
import tempfile

@pytest.fixture
def mock_groq_client():
    """Mock Groq client for testing"""
    mock = MagicMock()
    mock.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Test response"))]
    )
    return mock

@pytest.fixture
def mock_audio_file():
    """Create a temporary audio file for testing"""
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        f.write(b'dummy audio data')
        return f.name

@pytest.fixture
def test_patient_data():
    """Sample patient data for testing"""
    return {
        "name": "Test Patient",
        "age": 30,
        "symptoms": ["headache", "fever"],
        "medical_history": "No significant medical history"
    }

@pytest.fixture
def mock_conversation_history():
    """Sample conversation history for testing"""
    return [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi, how can I help you today?"}
    ] 