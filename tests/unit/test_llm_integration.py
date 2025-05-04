import pytest
from utils.groq_integration import get_groq_response
from unittest.mock import patch, MagicMock

def test_get_groq_response_success(mock_conversation_history):
    """Test successful LLM response generation"""
    with patch('utils.groq_integration.groq') as mock_groq:
        # Mock the Groq response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_groq.return_value.chat.completions.create.return_value = mock_response

        # Test response generation
        result = get_groq_response(
            input_text="Hello",
            model="llama3-8b-8192",
            history=mock_conversation_history
        )
        assert result == "Test response"
        mock_groq.return_value.chat.completions.create.assert_called_once()

def test_get_groq_response_with_system_prompt(mock_conversation_history):
    """Test LLM response generation with system prompt"""
    with patch('utils.groq_integration.groq') as mock_groq:
        # Mock the Groq response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_groq.return_value.chat.completions.create.return_value = mock_response

        # Test response generation with system prompt
        system_prompt = "You are a helpful medical assistant."
        result = get_groq_response(
            input_text="Hello",
            model="llama3-8b-8192",
            history=mock_conversation_history,
            system_prompt=system_prompt
        )
        assert result == "Test response"
        mock_groq.return_value.chat.completions.create.assert_called_once()

def test_get_groq_response_error(mock_conversation_history):
    """Test LLM response generation with API error"""
    with patch('utils.groq_integration.groq') as mock_groq:
        # Mock API error
        mock_groq.return_value.chat.completions.create.side_effect = Exception("API Error")

        # Test response generation
        result = get_groq_response(
            input_text="Hello",
            model="llama3-8b-8192",
            history=mock_conversation_history
        )
        assert result is None 