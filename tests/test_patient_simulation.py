import pytest
from unittest.mock import patch, MagicMock
import json
from utils.patient_simulation import PatientSimulator

@pytest.fixture
def mock_patient_data():
    """Fixture for mock patient data"""
    return {
        "name": "John Doe",
        "age": 45,
        "symptoms": ["headache", "fever"],
        "medical_history": ["hypertension"],
        "current_medications": ["aspirin"]
    }

@pytest.fixture
def mock_groq_response():
    """Fixture for mock Groq API response"""
    return {
        "choices": [{
            "message": {
                "content": "I'm feeling better today."
            }
        }]
    }

def test_patient_initialization(mock_patient_data):
    """Test patient simulator initialization"""
    simulator = PatientSimulator(mock_patient_data)
    
    # Verify patient data
    assert simulator.name == mock_patient_data["name"]
    assert simulator.age == mock_patient_data["age"]
    assert simulator.symptoms == mock_patient_data["symptoms"]
    assert simulator.medical_history == mock_patient_data["medical_history"]
    assert simulator.current_medications == mock_patient_data["current_medications"]

def test_generate_response(mock_patient_data, mock_groq_response):
    """Test response generation from patient simulator"""
    with patch('utils.patient_simulation.requests.post') as mock_post:
        # Configure mock
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_groq_response
        
        # Initialize simulator and generate response
        simulator = PatientSimulator(mock_patient_data)
        response = simulator.generate_response("How are you feeling today?")
        
        # Verify response
        assert response == "I'm feeling better today."
        mock_post.assert_called_once()

def test_generate_response_with_history(mock_patient_data, mock_groq_response):
    """Test response generation with conversation history"""
    with patch('utils.patient_simulation.requests.post') as mock_post:
        # Configure mock
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_groq_response
        
        # Initialize simulator with history
        simulator = PatientSimulator(mock_patient_data)
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I help you?"}
        ]
        
        # Generate response with history
        response = simulator.generate_response("How are you feeling?", history)
        
        # Verify response and history
        assert response == "I'm feeling better today."
        mock_post.assert_called_once()
        
        # Verify history was included
        call_args = mock_post.call_args[1]['json']
        assert "messages" in call_args
        assert len(call_args["messages"]) > 2  # Should include history plus current message

def test_generate_response_error_handling(mock_patient_data):
    """Test error handling in response generation"""
    with patch('utils.patient_simulation.requests.post') as mock_post:
        # Configure mock for error
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {"error": "API Error"}
        
        # Initialize simulator and test error handling
        simulator = PatientSimulator(mock_patient_data)
        response = simulator.generate_response("How are you feeling?")
        
        # Verify error handling
        assert response == "I apologize, but I'm having trouble responding right now."
        mock_post.assert_called_once()

def test_generate_response_network_error(mock_patient_data):
    """Test network error handling"""
    with patch('utils.patient_simulation.requests.post') as mock_post:
        # Configure mock for network error
        mock_post.side_effect = Exception("Network error")
        
        # Initialize simulator and test network error
        simulator = PatientSimulator(mock_patient_data)
        response = simulator.generate_response("How are you feeling?")
        
        # Verify error handling
        assert response == "I apologize, but I'm having trouble responding right now."
        mock_post.assert_called_once()

def test_update_patient_state(mock_patient_data):
    """Test updating patient state"""
    simulator = PatientSimulator(mock_patient_data)
    
    # Update patient state
    new_symptoms = ["headache", "nausea"]
    simulator.update_state({"symptoms": new_symptoms})
    
    # Verify state update
    assert simulator.symptoms == new_symptoms
    assert simulator.name == mock_patient_data["name"]  # Other fields should remain unchanged

def test_get_patient_summary(mock_patient_data):
    """Test getting patient summary"""
    simulator = PatientSimulator(mock_patient_data)
    
    # Get patient summary
    summary = simulator.get_summary()
    
    # Verify summary format
    assert isinstance(summary, str)
    assert mock_patient_data["name"] in summary
    assert str(mock_patient_data["age"]) in summary
    for symptom in mock_patient_data["symptoms"]:
        assert symptom in summary 