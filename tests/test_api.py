import os
import sys
import unittest
import json
from io import BytesIO
import tempfile
from unittest.mock import patch, MagicMock

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Create a test audio file
        self.test_audio = os.path.join(tempfile.gettempdir(), 'test_audio.wav')
        with open(self.test_audio, 'wb') as f:
            # Write a simple WAV header
            f.write(b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xAC\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')

    def tearDown(self):
        # Remove test audio file
        if os.path.exists(self.test_audio):
            os.remove(self.test_audio)

    def test_index_route(self):
        """Test the main route returns the HTML page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)
        
    def test_process_audio_no_file(self):
        """Test the /process_audio route without a file"""
        response = self.client.post('/process_audio')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        
    def test_process_audio_with_file(self):
        """Test the /process_audio route with a file"""
        # Skip this test if GROQ_API_KEY is not set
        if not os.environ.get('GROQ_API_KEY'):
            self.skipTest('GROQ_API_KEY not set in environment variables')
            
        with open(self.test_audio, 'rb') as f:
            data = {'audio': (BytesIO(f.read()), 'test_audio.wav')}
            response = self.client.post(
                '/process_audio',
                data=data,
                content_type='multipart/form-data'
            )
            
        # This should return a 200 status code, but the actual transcription might fail
        # We're just testing that the API endpoint functions correctly
        self.assertEqual(response.status_code, 200)
    
    @patch('app.transcribe_audio_data')
    @patch('app.get_groq_response')
    @patch('app.generate_speech_audio')
    @patch('app.get_conversation')
    @patch('app.update_conversation_title')
    def test_content_based_title_update(self, mock_update_title, mock_get_conversation, 
                                       mock_generate_speech, mock_get_response, mock_transcribe):
        """Test that conversation title is updated based on first message content"""
        # Mock the audio transcription to return a test message
        test_message = "This is a test message for content-based title"
        mock_transcribe.return_value = test_message
        
        # Mock the LLM response
        mock_get_response.return_value = "This is a test response"
        
        # Mock the speech generation
        mock_generate_speech.return_value = b'test audio bytes'
        
        # Mock conversation data with two messages to simulate first exchange
        mock_get_conversation.return_value = {
            'id': 1,
            'title': 'New Conversation',
            'messages': [
                {'role': 'user', 'content': test_message},
                {'role': 'assistant', 'content': 'This is a test response'}
            ]
        }
        
        # Send a test audio file
        with open(self.test_audio, 'rb') as f:
            data = {'audio': (BytesIO(f.read()), 'test_audio.wav')}
            self.client.post(
                '/process_audio',
                data=data,
                content_type='multipart/form-data'
            )
        
        # Verify that update_conversation_title was called with the first 30 chars
        expected_title = test_message[:30] + "..." if len(test_message) > 30 else test_message
        mock_update_title.assert_called_once()
        args, _ = mock_update_title.call_args
        self.assertEqual(args[1], expected_title)
        
if __name__ == '__main__':
    unittest.main() 