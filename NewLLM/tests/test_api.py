import os
import sys
import unittest
import json
from io import BytesIO
import tempfile

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
        
if __name__ == '__main__':
    unittest.main() 