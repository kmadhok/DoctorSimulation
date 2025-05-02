import pytest
from unittest.mock import patch, MagicMock
import os
from utils.environment import EnvironmentConfig

@pytest.fixture
def mock_env_vars():
    """Fixture for mock environment variables"""
    return {
        "GROQ_API_KEY": "test_api_key",
        "OPENAI_API_KEY": "test_openai_key",
        "ELEVENLABS_API_KEY": "test_elevenlabs_key",
        "DEBUG_MODE": "true"
    }

def test_environment_initialization(mock_env_vars):
    """Test environment configuration initialization"""
    with patch.dict(os.environ, mock_env_vars):
        config = EnvironmentConfig()
        
        # Verify environment variables
        assert config.groq_api_key == mock_env_vars["GROQ_API_KEY"]
        assert config.openai_api_key == mock_env_vars["OPENAI_API_KEY"]
        assert config.elevenlabs_api_key == mock_env_vars["ELEVENLABS_API_KEY"]
        assert config.debug_mode is True

def test_missing_required_variables():
    """Test handling of missing required environment variables"""
    with patch.dict(os.environ, {}, clear=True):
        config = EnvironmentConfig()
        
        # Verify default values
        assert config.groq_api_key is None
        assert config.openai_api_key is None
        assert config.elevenlabs_api_key is None
        assert config.debug_mode is False

def test_invalid_debug_mode():
    """Test handling of invalid debug mode value"""
    with patch.dict(os.environ, {"DEBUG_MODE": "invalid"}):
        config = EnvironmentConfig()
        
        # Verify debug mode defaults to False for invalid values
        assert config.debug_mode is False

def test_validate_environment(mock_env_vars):
    """Test environment validation"""
    with patch.dict(os.environ, mock_env_vars):
        config = EnvironmentConfig()
        
        # Test validation
        is_valid, missing_vars = config.validate_environment()
        
        # Verify validation results
        assert is_valid is True
        assert len(missing_vars) == 0

def test_validate_environment_missing_vars():
    """Test environment validation with missing variables"""
    with patch.dict(os.environ, {}, clear=True):
        config = EnvironmentConfig()
        
        # Test validation
        is_valid, missing_vars = config.validate_environment()
        
        # Verify validation results
        assert is_valid is False
        assert len(missing_vars) > 0
        assert "GROQ_API_KEY" in missing_vars
        assert "OPENAI_API_KEY" in missing_vars
        assert "ELEVENLABS_API_KEY" in missing_vars

def test_get_api_key(mock_env_vars):
    """Test getting API key"""
    with patch.dict(os.environ, mock_env_vars):
        config = EnvironmentConfig()
        
        # Test getting Groq API key
        groq_key = config.get_api_key("GROQ_API_KEY")
        assert groq_key == mock_env_vars["GROQ_API_KEY"]
        
        # Test getting non-existent key
        non_existent_key = config.get_api_key("NON_EXISTENT_KEY")
        assert non_existent_key is None

def test_is_debug_mode(mock_env_vars):
    """Test debug mode check"""
    with patch.dict(os.environ, mock_env_vars):
        config = EnvironmentConfig()
        
        # Test debug mode
        assert config.is_debug_mode() is True
        
        # Test non-debug mode
        with patch.dict(os.environ, {"DEBUG_MODE": "false"}):
            config = EnvironmentConfig()
            assert config.is_debug_mode() is False

def test_get_environment_summary(mock_env_vars):
    """Test getting environment summary"""
    with patch.dict(os.environ, mock_env_vars):
        config = EnvironmentConfig()
        
        # Get environment summary
        summary = config.get_environment_summary()
        
        # Verify summary format
        assert isinstance(summary, str)
        assert "Environment Configuration" in summary
        assert "Debug Mode: True" in summary
        assert "API Keys Configured: Yes" in summary 