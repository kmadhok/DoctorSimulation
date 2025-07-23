# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
python app.py --port 8001
```

### Testing
```bash
# Run all tests
python -m pytest

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/

# Run individual test files
python test_patient_simulation.py
```

### Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Install Node.js dependencies for VAD (Voice Activity Detection)
npm install
```

## Architecture Overview

This is a Flask-based voice conversation application designed for **single-agent persona conversations**. Users can select from different AI personas and engage in deep, voice-based conversations with their chosen personality type.

### Core Architecture

**Persona-Based Conversation System**
The application centers around one-on-one conversations between users and AI agents with distinct personalities:

- **Persona Selection**: Dropdown interface allows users to choose from 6 different personality types
- **Voice-First Interaction**: Real-time voice-to-voice conversations using Groq APIs
- **Conversation Persistence**: All conversations stored in SQLite database for history and analysis
- **Character Consistency**: Each persona maintains distinct speaking styles, worldviews, and response patterns

**Voice Processing Pipeline**
- **Client-Side VAD**: `static/vad-model/` contains Silero VAD models for real-time speech detection
- **Barge-In Functionality**: Users can interrupt agent speech naturally during conversation
- **Audio Queue Management**: Prevents audio conflicts and manages smooth conversation flow
- **Groq Integration**: Transcription (Whisper), LLM (Llama), and TTS all use Groq APIs

**Persona System (`utils/persona_system.py`)**
Six distinct personalities with rich characteristics:
- **Marcus** (Wise Mentor): Patient, thoughtful guidance with life lessons
- **Luna** (Creative Artist): Imaginative, passionate with artistic perspective
- **Alex** (Tech Innovator): Analytical, optimistic about technology solutions
- **Sage** (Mindful Philosopher): Contemplative, focuses on deeper meaning
- **Jordan** (Enthusiastic Coach): Energetic, motivational with sports metaphors
- **Riley** (Witty Comedian): Humorous, observational with clever wordplay

Each persona includes:
- Personality traits and speaking style
- Worldview and background story
- Response patterns and conversational approach
- Unique voice ID for TTS consistency

**Flask Application (`app.py`)**
- `/process_audio` - Main endpoint for voice conversation processing
- `/api/select-persona` - Persona selection and conversation initialization
- `/api/conversations` - Conversation history management
- Request ID tracking prevents race conditions during voice interruptions

### Key Components

**Database Layer (`utils/database.py`)**
- SQLite database with conversation persistence
- Stores persona data, conversation history, and metadata
- Supports conversation loading and management
- Foundation for user profiling across conversations

**Frontend Architecture**
- **Real-Time Audio**: `static/js/main.js` manages VAD, audio recording, and playback
- **Persona Interface**: Dropdown selection with persona descriptions
- **Voice Activity Detection**: Silero models for natural speech detection
- **Audio Context API**: Web Audio API for TTS playback and interruption handling

**Voice Processing (`utils/groq_*.py`)**
- `groq_transcribe.py` - Speech-to-text using Groq Whisper API
- `groq_integration.py` - LLM conversation processing with history
- `groq_tts_speech.py` - Text-to-speech with persona-specific voices

### Development Notes

**Conversation Flow**:
1. User selects persona from dropdown
2. Voice conversation begins with persona-specific system prompt
3. Real-time voice processing with interruption support
4. All interactions stored in database for persistence

**Race Condition Prevention**:
- `activeRequestId` prevents outdated server responses
- `activeAudioSourceId` prevents audio conflicts
- Barge-in handling immediately stops agent speech

**Future Enhancement Areas**:
- User profiling system will analyze conversation patterns across all personas
- Right-hand sidebar for user personality insights
- Cross-conversation analysis and summarization

### Environment Setup

Required environment variables:
- `GROQ_API_KEY` - Groq API key for LLM, transcription, and TTS services

Database: SQLite (`conversations.db`) for persistent conversation history

### Testing Structure
- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests for conversation flows
- Individual test files for specific functionality testing