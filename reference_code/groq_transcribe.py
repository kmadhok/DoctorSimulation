import os
import tempfile
import wave
import numpy as np
import sounddevice as sd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def groq_transcribe_from_microphone(duration=5, model="whisper-large-v3-turbo"):
    """
    Record audio from microphone, transcribe it using Groq API, and return the transcription.
    
    Args:
        duration (int): Recording duration in seconds
        model (str): Groq Whisper model to use (whisper-large-v3-turbo, distil-whisper-large-v3-en, whisper-large-v3)
    
    Returns:
        str: Transcribed speech or None if no speech detected
    """
    try:
        # Initialize the Groq client

        api_key = os.environ.get('GROQ_API_KEY')
        client = Groq(api_key=api_key)
        
        print("Recording audio...")
        # Record audio for transcription
        audio_data, sample_rate = record_audio(duration=duration)
        
        # Save to temporary file
        temp_file = save_audio_to_temp_file(audio_data, sample_rate)
        
        # Transcribe with Groq API
        print(f"Transcribing audio using Groq API with model: {model}...")
        with open(temp_file, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(temp_file, file.read()),  # Required audio file
                model=model,  # Required model to use for transcription
                temperature=0.0  # Optional parameter
            )
        
        # Clean up temporary file
        os.remove(temp_file)
        
        # Extract text from transcription response
        transcription_text = transcription.text
        
        return transcription_text.strip() if transcription_text.strip() else None
        
    except KeyboardInterrupt:
        print("\nExiting...")
        return None

def record_audio(duration=5, sample_rate=16000, channels=1):
    """
    Record audio from microphone.
    
    Args:
        duration (int): Recording duration in seconds
        sample_rate (int): Sample rate in Hz
        channels (int): Number of audio channels
    
    Returns:
        numpy.ndarray: Recorded audio data
        int: Sample rate
    """
    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Recording finished")
    return audio_data, sample_rate


def save_audio_to_temp_file(audio_data, sample_rate, channels=1):
    """
    Save recorded audio to a temporary WAV file.
    
    Args:
        audio_data (numpy.ndarray): Audio data
        sample_rate (int): Sample rate in Hz
        channels (int): Number of audio channels
        
    Returns:
        str: Path to the temporary WAV file
    """
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_file.close()
    
    with wave.open(temp_file.name, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        # Convert float32 array to int16
        audio_data_int = (audio_data * 32767).astype(np.int16)
        wf.writeframes(audio_data_int.tobytes())
    
    return temp_file.name

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Transcribe speech from microphone using Groq API")
    parser.add_argument("--duration", type=int, default=5,
                        help="Recording duration in seconds")
    parser.add_argument("--model", type=str, default="whisper-large-v3-turbo", 
                        choices=["whisper-large-v3-turbo", "distil-whisper-large-v3-en", "whisper-large-v3"],
                        help="Groq Whisper model to use")
    
    args = parser.parse_args()
    
    # Transcribe from microphone using Groq API
    transcription = groq_transcribe_from_microphone(
        duration=args.duration,
        model=args.model
    )
    
    if transcription:
        print(f"\nTranscription: {transcription}")
    else:
        print("\nNo transcription was produced.")