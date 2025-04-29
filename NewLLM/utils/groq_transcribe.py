import os
import tempfile
import wave
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio_data(audio_bytes, model="whisper-large-v3-turbo"):
    """
    Transcribe audio data using Groq API.
    
    Args:
        audio_bytes (bytes): Raw audio data in bytes
        model (str): Groq Whisper model to use
    
    Returns:
        str: Transcribed text or empty string if transcription failed
    """
    try:
        # Get API key from environment
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            print("Error: GROQ_API_KEY not set in environment variables")
            return ""
        
        # Save audio bytes to temporary file for API
        temp_file = save_audio_bytes_to_temp_file(audio_bytes)
        
        # Prepare API request
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        print(f"Transcribing audio using Groq API with model: {model}...")
        
        # Create form data with the file and model
        with open(temp_file, "rb") as file:
            files = {
                "file": file,
                "model": (None, model),
                "response_format": (None, "json"),
                "temperature": (None, "0.0")
            }
            
            # Make the API request
            response = requests.post(url, headers=headers, files=files)
            
            # Check for successful response
            if response.status_code == 200:
                transcription_data = response.json()
                transcription_text = transcription_data.get("text", "")
            else:
                print(f"Error from Groq API: Status {response.status_code}")
                print(f"Response: {response.text}")
                transcription_text = ""
        
        # Clean up temporary file
        os.remove(temp_file)
        
        return transcription_text.strip() if transcription_text.strip() else ""
        
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return ""

def save_audio_bytes_to_temp_file(audio_bytes):
    """
    Save audio bytes to a temporary WAV file.
    
    Args:
        audio_bytes (bytes): Raw audio data
        
    Returns:
        str: Path to the temporary WAV file
    """
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_file.write(audio_bytes)
    temp_file.close()
    
    return temp_file.name

# Keep the original implementation for command-line usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Transcribe speech from a WAV file using Groq API")
    parser.add_argument("--file", type=str, required=True,
                        help="Path to WAV file to transcribe")
    parser.add_argument("--model", type=str, default="whisper-large-v3-turbo", 
                        choices=["whisper-large-v3-turbo", "distil-whisper-large-v3-en", "whisper-large-v3"],
                        help="Groq Whisper model to use")
    
    args = parser.parse_args()
    
    # Read audio file
    with open(args.file, "rb") as f:
        audio_bytes = f.read()
    
    # Transcribe audio
    transcription = transcribe_audio_data(audio_bytes, args.model)
    
    if transcription:
        print(f"\nTranscription: {transcription}")
    else:
        print("\nNo transcription was produced.") 