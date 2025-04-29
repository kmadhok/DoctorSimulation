import os
import argparse
import tempfile
import wave
import sys
import threading
import queue
import time
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from collections import deque
#from new_approach.archive.transcribe import no_wake_transcribe_from_microphone_simplified,record_audio, save_audio_to_temp_file, transcribe_audio, transcribe_from_microphone_simplified
from groq_integration import get_llm_response, get_groq_response
#from tts_speech import text_to_speech
from groq_transcribe import groq_transcribe_from_microphone
from groq_tts_speech import text_to_speech


# transcribe = transcribe_from_microphone_simplified()
# print(transcribe)
# response = get_llm_response(transcribe)
# print(response)
# text_to_speech(response)

# Simple welcome message
print("Starting conversation. Say 'exit' or 'quit' to end.")

conversation_history = []
user_history = []
llm_history = []
history = []
# Combine user and llm messages into conversation history
for user_msg, llm_msg in zip(user_history, llm_history):
    conversation_history.append({
        "role": "user",
        "content": user_msg
    })
    conversation_history.append({
        "role": "assistant", 
        "content": llm_msg
    })

# while True:
#     # Get user input
#     print("\nListening...")
#     #transcribe = transcribe_from_microphone_simplified()
#     transcribe = no_wake_transcribe_from_microphone_simplified()
#     print(f"You said: {transcribe}")

#     # Check if user wants to exit
#     if "exit" in transcribe.lower() or "quit" in transcribe.lower():
#         print("Ending conversation. Goodbye!")
#         break
    
#     # Compare current transcription with the most recent LLM response
#     if llm_history and transcribe.lower() == llm_history[-1].lower():
#         print("You repeated what I just said!")
#         response = "It seems you're repeating what I just said. Do you have a question about that?"
#     else:
#         # Add the transcription to user history
#         user_history.append(transcribe)
#         # Get LLM response based on current transcription
#         #response = get_llm_response(transcribe)
#         response = get_groq_response(transcribe, history)
#         # Add the response to LLM history
#         llm_history.append(response)
#             # Update history with both user input and assistant response
#         history.append({"role": "user", "content": transcribe})
#         history.append({"role": "assistant", "content": response})
    
#     user_history.append(transcribe)
#     # Check if user wants to exit
#     if "exit" in transcribe.lower() or "quit" in transcribe.lower():
#         print("Ending conversation. Goodbye!")
#         break
    
#     # Get LLM response based on current transcription only
#     response = get_llm_response(transcribe)
#     print(f"Assistant: {response}")
#     llm_history.append(response)
#     # Speak the response
#     text_to_speech(response)
while True:
    print("\nListening...")
    #transcribe = no_wake_transcribe_from_microphone_simplified()
    transcribe = groq_transcribe_from_microphone()
    print(f"You said: {transcribe}")

    if "exit" in transcribe.lower() or "quit" in transcribe.lower():
        print("Ending conversation. Goodbye!")
        break

    if llm_history and transcribe.lower() == llm_history[-1].lower():
        print("You repeated what I just said!")
        response = "It seems you're repeating what I just said. Do you have a question about that?"
    else:
        # Get response WITH history
        response = get_groq_response(
            input_text=transcribe,
            model="llama3-8b-8192",  # Specify model here
            history=history
        )
    
    # Update BOTH histories
    llm_history.append(response)
    history.append({"role": "user", "content": transcribe})
    history.append({"role": "assistant", "content": response})
    
    print(f"Assistant: {response}")
    text_to_speech(response)