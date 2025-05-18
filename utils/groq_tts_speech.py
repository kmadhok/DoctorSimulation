import os
import tempfile
import requests
import json
from dotenv import load_dotenv

load_dotenv()
import logging

logger = logging.getLogger(__name__) # Use __name__ for module-specific logger

def generate_speech_audio(text, voice_id="Fritz-PlayAI"):
    logger.debug(f"generate_speech_audio called for text: '{text[:50]}...'")
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        logger.error("Groq API key not found. Set GROQ_API_KEY environment variable.")
        return None
    
    try:
        url = "https://api.groq.com/openai/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "playai-tts", # Or "tts-1"
            "voice": voice_id,     # Or a standard voice like "alloy"
            "input": text,
            "response_format": "mp3" # You mentioned you changed to mp3
        }
        
        logger.debug(f"Making POST request to Groq TTS: {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=60) 
        logger.debug(f"Groq TTS response status: {response.status_code}")
        
        if response.status_code == 200:
            logger.debug("Starting to access response.content (all bytes downloaded)")
            audio_bytes = response.content
            logger.debug(f"Accessed response.content, size: {len(audio_bytes)} bytes")

            # ---- START OF TEMPORARY DEBUG CODE TO SAVE FILE ----
            try:
                # Ensure the filename matches the response_format
                debug_filename = "debug_tts_output.mp3" 
                with open(debug_filename, "wb") as f:
                    f.write(audio_bytes)
                logger.info(f"Successfully saved TTS audio to {debug_filename}")
            except Exception as e_save:
                logger.error(f"Error saving debug TTS audio file: {e_save}")
            # ---- END OF TEMPORARY DEBUG CODE TO SAVE FILE ----
            
            return audio_bytes
        else:
            logger.error(f"Error from Groq API: Status {response.status_code}, Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error("Groq TTS request timed out.")
        return None
    except requests.exceptions.RequestException as e: 
        logger.error(f"Error in text-to-speech (requests): {e}", exc_info=True)
        return None
    except Exception as e: 
        logger.error(f"Unexpected error in text-to-speech: {e}", exc_info=True)
        return None
# def generate_speech_audio(text, voice_id="Fritz-PlayAI"):
#     """
#     Convert text to speech using Groq API and return audio bytes.
    
#     Args:
#         text (str): The text to convert to speech
#         voice_id (str): The voice to use (default: Fritz-PlayAI)
        
#     Returns:
#         bytes: Audio data as bytes or None if generation fails
#     """
#     # Get Groq API key from environment variable
#     api_key = os.environ.get("GROQ_API_KEY")
    
#     # Check if API key is available
#     if not api_key:
#         print("Error: Groq API key not found. Set GROQ_API_KEY environment variable.")
#         return None
    
#     try:
#         # Prepare API request
#         url = "https://api.groq.com/openai/v1/audio/speech"
#         headers = {
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         }
        
#         # Prepare request payload
#         payload = {
#             "model": "playai-tts",
#             "voice": voice_id,
#             "input": text,
#             "response_format": "mp3"

#         }
        
#         # Make the API request
#         response = requests.post(url, headers=headers, json=payload)
        
#         # Check for successful response
#         if response.status_code == 200:
#             # Get audio bytes directly from response
#             audio_bytes = response.content
#             return audio_bytes
#         else:
#             print(f"Error from Groq API: Status {response.status_code}")
#             print(f"Response: {response.text}")
#             return None
        
#     except Exception as e:
#         print(f"Error in text-to-speech: {e}")
#         return None

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate speech from text using Groq API")
    parser.add_argument("--text", type=str, help="Text to convert to speech")
    parser.add_argument("--voice", type=str, default="Fritz-PlayAI", help="Voice ID to use")
    parser.add_argument("--output", type=str, help="Output file path (WAV format)")
    
    args = parser.parse_args()
    
    # Get text from arguments, stdin, or prompt
    if args.text:
        input_text = args.text
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
    else:
        input_text = input("Enter text to speak: ")
    
    if not input_text.strip():
        print("Error: No input text provided.")
        sys.exit(1)
    
    # Generate speech audio
    audio_bytes = generate_speech_audio(input_text, args.voice)
    
    if audio_bytes:
        if args.output:
            # Save to specified output file
            with open(args.output, 'wb') as f:
                f.write(audio_bytes)
            print(f"Audio saved to {args.output}")
        else:
            # Save to default output file
            output_file = "output.wav"
            with open(output_file, 'wb') as f:
                f.write(audio_bytes)
            print(f"Audio saved to {output_file}")
    else:
        print("Failed to generate speech audio.") 