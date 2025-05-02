import pytest
from unittest.mock import patch, MagicMock
import json
import os
from utils.groq_integration import get_groq_response

@pytest.fixture
def mock_groq_response():
    """Fixture for mock Groq API response"""
    return {
        'choices': [{
            'message': {
                'content': 'Test response'
            }
        }]
    }

@pytest.fixture
def mock_error_response():
    """Fixture for mock error response"""
    return {
        'error': {
            'message': 'API Error'
        }
    }

def test_groq_response_generation(mock_groq_response):
    """Test successful LLM response generation"""
    with patch('utils.groq_integration.requests.post') as mock_post:
        # Configure mock
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_groq_response
        
        # Test response generation
        response = get_groq_response(
            input_text="Test input",
            model="llama3-8b-8192"
        )
        
        # Verify response
        assert response == "Test response"
        mock_post.assert_called_once()

def test_groq_response_with_history(mock_groq_response):
    """Test LLM response with conversation history"""
    # Setup test data
    history = [
        {"role": "user", "content": "Previous question"},
        {"role": "assistant", "content": "Previous answer"}
    ]
    
    with patch('utils.groq_integration.requests.post') as mock_post:
        # Configure mock
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_groq_response
        
        # Test response generation with history
        response = get_groq_response(
            input_text="Test input",
            model="llama3-8b-8192",
            history=history
        )
        
        # Verify response and request
        assert response == "Test response"
        mock_post.assert_called_once()
        
        # Verify history was included in request
        call_args = mock_post.call_args[1]['json']
        assert 'messages' in call_args
        assert len(call_args['messages']) == 3  # System + 2 history messages

def test_groq_response_with_system_prompt(mock_groq_response):
    """Test LLM response with system prompt"""
    system_prompt = "You are a helpful medical assistant."
    
    with patch('utils.groq_integration.requests.post') as mock_post:
        # Configure mock
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_groq_response
        
        # Test response generation with system prompt
        response = get_groq_response(
            input_text="Test input",
            model="llama3-8b-8192",
            system_prompt=system_prompt
        )
        
        # Verify response and request
        assert response == "Test response"
        mock_post.assert_called_once()
        
        # Verify system prompt was included
        call_args = mock_post.call_args[1]['json']
        assert 'messages' in call_args
        assert call_args['messages'][0]['role'] == 'system'
        assert call_args['messages'][0]['content'] == system_prompt

def test_groq_response_error_handling(mock_error_response):
    """Test error handling in LLM response generation"""
    with patch('utils.groq_integration.requests.post') as mock_post:
        # Configure mock for error
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = mock_error_response
        
        # Test error handling
        response = get_groq_response(
            input_text="Test input",
            model="llama3-8b-8192"
        )
        
        # Verify error handling
        assert response == "Error: API Error"
        mock_post.assert_called_once()

def test_groq_response_network_error():
    """Test network error handling"""
    with patch('utils.groq_integration.requests.post') as mock_post:
        # Configure mock for network error
        mock_post.side_effect = Exception("Network error")
        
        # Test network error handling
        response = get_groq_response(
            input_text="Test input",
            model="llama3-8b-8192"
        )
        
        # Verify error handling
        assert response == "Error: Network error"
        mock_post.assert_called_once()

def test_groq_response_missing_api_key():
    """Test handling of missing API key"""
    # Save original API key
    original_key = os.environ.get('GROQ_API_KEY')
    
    try:
        # Remove API key
        if 'GROQ_API_KEY' in os.environ:
            del os.environ['GROQ_API_KEY']
        
        # Test missing API key handling
        response = get_groq_response(
            input_text="Test input",
            model="llama3-8b-8192"
        )
        
        # Verify error handling
        assert response == "Error: GROQ_API_KEY not found in environment"
        
    finally:
        # Restore original API key
        if original_key:
            os.environ['GROQ_API_KEY'] = original_key 