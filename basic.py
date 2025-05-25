# app.py
import os
import io
import json
import time
from uuid import uuid4
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException, Response
from fastapi.middleware.gzip import GZipMiddleware
from groq import Groq

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Initialize Groq client
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

@app.post("/transcribe/")
async def transcribe(
    audio: UploadFile = File(...),
    messageHistory: Optional[str] = Form(None),
    ttsEnabled: Optional[str]    = Form("true"),
    x_skip_audio: Optional[str]  = Header(None, alias="X-Skip-Audio"),
):
    request_id = uuid4().hex[:8]
    print(f"[{request_id}] Starting request")

    # 1. Read & validate audio
    content = await audio.read()
    if not content:
        raise HTTPException(400, "No audio file provided")
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(413, "Audio file too large")

    # 2. Transcribe via Groq Whisper
    t0 = time.perf_counter()
    transcription = groq.audio.transcriptions.create(
        file=(audio.filename or "audio.wav", content),
        model="whisper-large-v3",
    )
    transcript = transcription.text.strip()
    if not transcript:
        raise HTTPException(400, "No speech detected in audio")
    print(f"[{request_id}] Transcribed in {time.perf_counter() - t0:.2f}s")

    # 3. Build chat history & get LLM response
    try:
        history: List[Dict[str, Any]] = json.loads(messageHistory) if messageHistory else []
    except json.JSONDecodeError:
        history = []

    system_prompt = (
        "You are a helpful voice AI assistant.\n"
        "- The user is speaking through a microphone.\n"
        "- Respond briefly; do not add unnecessary info.\n"
        "- If you don't understand, ask for clarification.\n"
        f"- Today's date is {time.strftime('%Y-%m-%d')}.\n"
        "- Keep responses concise."
    )
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": transcript})

    t1 = time.perf_counter()
    completion = groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
    )
    response_text = completion.choices[0].message.content or ""
    print(f"[{request_id}] LLM responded in {time.perf_counter() - t1:.2f}s")

    # 4. Check skip‑audio flag
    skip_audio = (x_skip_audio == "true") or (ttsEnabled.lower() != "true")
    if skip_audio:
        return {
            "transcript": transcript,
            "response": response_text,
            "audioUrl": None
        }

    # 5. Generate TTS via Groq playai-tts
    t2 = time.perf_counter()
    tts_result = groq.audio.speech.create(
        model="playai-tts",
        voice="Fritz-PlayAI",       # pick from the available voices
        input=response_text,
        response_format="wav"
    )
    print(f"[{request_id}] TTS generated in {time.perf_counter() - t2:.2f}s")

    # 6. Stream back the WAV
    wav_bytes = tts_result.read()  # returns the raw WAV bytes
    return Response(
        content=wav_bytes,
        media_type="audio/wav",
        headers={
            "X-Transcript": transcript,
            "X-Response": response_text,
        },
    )
