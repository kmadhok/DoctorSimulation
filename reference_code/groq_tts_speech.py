import io
from pydub import AudioSegment
from pydub.playback import play
import os
from groq import Groq

def text_to_speech(text, voice_id="Fritz-PlayAI"):
    """
    Convert text to speech using Groq API and play it directly.
    
    Args:
        text (str): The text to convert to speech
        voice_id (str): The voice to use (default: Fritz-PlayAI)
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Get Groq API key from environment variable

    api_key = os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    # Check if API key is available
    # if not groq_api_key:
    #     print("Error: Groq API key not found. Set GROQ_API_KEY environment variable.")
    #     return False
    
    try:
        # Initialize Groq client
        # client = Groq(api_key=groq_api_key)
        
        # Create a temporary file path for the audio
        temp_file_path = "temp_speech.wav"
        
        # Request speech synthesis
        response = client.audio.speech.create(
            model="playai-tts",
            voice=voice_id,
            input=text,
            response_format="wav"
        )
        
        # Save audio to temporary file
        response.write_to_file(temp_file_path)
        
        # Load the audio file using pydub
        sound = AudioSegment.from_file(temp_file_path, format="wav")
        
        print(f"\n🔈 Speaking: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        # Play the audio
        play(sound)
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        return True
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return False

def generate_tts_audio(text):
    """Generates TTS audio and returns it as bytes."""
    try:
        # Assuming your groq_tts_speech.text_to_speech function is already
        # adapted to SAVE or RETURN audio data instead of playing it.
        # If it saves to a file, read the bytes from the file.
        # If it returns bytes directly, use that.
        # Example: Assuming it saves to 'output.mp3'
        output_filename = "output.mp3" # Or whatever your function saves as
        text_to_speech(text) # Call the original function

        if os.path.exists(output_filename):
             with open(output_filename, 'rb') as f:
                 audio_bytes = f.read()
             os.remove(output_filename) # Clean up the temporary file
             return audio_bytes
        else:
             print("Error: TTS did not generate an output file.")
             return None

        # --- OR ---
        # If your modified groq_tts function returns bytes directly:
        # audio_bytes = groq_tts(text)
        # return audio_bytes

    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    # If arguments are provided, use them as text
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
        text_to_speech(input_text)
    
    # If no arguments but stdin has data (piping), use that
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
        if input_text:
            text_to_speech(input_text)
    
    # Otherwise, prompt for input
    else:
        text = input("Enter text to speak: ")
        if text.strip():
            text_to_speech(text)