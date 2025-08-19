# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
python app.py --port 8001
```

### Testing
```bash
# Run comprehensive test suite (recommended)
python run_all_tests.py

# Run pytest suite
python -m pytest

# Run specific test categories  
python -m pytest tests/unit/
python -m pytest tests/integration/

# Run individual test files
python test_patient_simulation.py
python test_multi_agent.py
python test_integration_multi_agent.py
python test_standalone_crew_agents.py
python test_standalone_persona_system.py
```

### Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Install Node.js dependencies for VAD (Voice Activity Detection)
npm install
```

## Architecture Overview

This is a Flask-based voice conversation application designed for multi-agent AI conversations. The system operates like a **conference call** where users can engage in free-flowing conversations with multiple AI agents that have distinct personalities and can interact with each other naturally.

### Core Architecture

**Multi-Agent Conversation System**
The application centers around a sophisticated orchestration system that manages dynamic conversations between users and multiple AI agents:

- **Intelligent Speaker Selection**: `utils/crew_agents.py` contains `MultiAgentConversationOrchestrator` that uses LLM-based `_moderator_pick()` to decide which agent should respond based on context and expertise
- **Real-Time Interruption Handling**: VAD (Voice Activity Detection) triggers `handleUserBargeIn()` which immediately stops agent speech and clears the audio queue when users interrupt
- **Sequential Response Queue**: `audioQueue` system manages multiple agent responses with natural pacing between speakers
- **Context-Aware Agents**: Each agent maintains shared conversation memory and can reference previous speakers

**Voice Processing Pipeline**
- **Client-Side VAD**: `static/vad-model/` contains Silero VAD models for real-time speech detection
- **Barge-In Functionality**: `onSpeechStart` event immediately interrupts agent speech when user speaks
- **Audio Queue Management**: Sequential TTS playback with race condition prevention using `activeRequestId` and `activeAudioSourceId`
- **Groq Integration**: Transcription, LLM, and TTS all use Groq APIs for consistent voice processing

**Persona System**
- **Three Debate Personas**: Hope (Optimistic), Sage (Critical), Alex (Balanced) with rich personality traits
- **Dynamic Interaction**: Agents can address each other by name, build on previous points, and engage in natural dialogue
- **Context Adaptation**: Personas adapt their responses based on conversation history and user interaction patterns

**Flask Application (`app.py`)**
- `/process_audio_multi_agent` - Main endpoint for multi-agent conversations
- `/api/create-multi-agent-conversation` - Initialize multi-agent sessions  
- `/process_audio` - Single-agent voice conversations
- `/generate_patient_case` - AI-generated medical case creation
- Request ID tracking prevents server-side race conditions during interruptions
- Session-based conversation management with SQLite persistence
- Comprehensive logging (`app.log`) for debugging conversation flow

### Key Conversation Mechanics

**User Priority System**: Agents always defer to user input and can be interrupted at any time
**Agent-to-Agent Communication**: Agents can directly address each other and build collaborative responses
**Natural Conversation Flow**: 5-second idle timer triggers automatic agent responses to maintain conversation momentum
**Memory Sharing**: All agents access shared conversation history through `_get_recent_context()`

### Development Notes

**Race Condition Prevention**: The system uses multiple mechanisms to prevent audio playback conflicts:
- `activeRequestId` prevents processing outdated server responses
- `activeAudioSourceId` prevents late audio events from interfering
- `handleUserBargeIn()` immediately invalidates ongoing requests when users interrupt

**Conversation State Management**: 
- `currentConversationId` tracks active conversation sessions
- `audioQueue` maintains sequential agent responses
- `conversation_history` provides shared context for all agents

**Testing Structure**
- `run_all_tests.py` - Comprehensive test runner with detailed reporting
- `tests/unit/` - Unit tests for individual components (LLM, transcription, TTS)
- `tests/integration/` - Integration tests for conversation flows
- Standalone test files: `test_standalone_crew_agents.py`, `test_standalone_persona_system.py`
- Application tests: `test_multi_agent.py`, `test_patient_simulation.py`, `test_integration_multi_agent.py`

### Environment Setup

**Required Environment Variables**
- `GROQ_API_KEY` - Groq API key for LLM, transcription, and TTS services (obtain from [Groq Console](https://console.groq.com/keys))

**Database**
- SQLite (`conversations.db`) - Persistent conversation history and patient simulation data

**Key Dependencies**
- Flask 2.3.3 - Web framework
- CrewAI 0.130.0 - Multi-agent orchestration
- Groq 0.9.0 - LLM, transcription, and TTS APIs  
- pytest 7.4.3 - Testing framework
- Node.js - Required for VAD model setup (`npm install`)

### Frontend Architecture

**Real-Time Audio Processing**:
- `static/js/main.js` - 2000+ lines managing VAD, audio queue, and conversation state
- `MicVAD` integration with Silero models for speech detection
- `AudioContext` API for TTS playback and interruption handling
- WebRTC `getUserMedia()` for microphone access

**Multi-Agent Interface**:
- Conference call setup UI for selecting active agents
- Real-time speaking indicators showing which agent is active  
- User controls for pausing, interrupting, and managing conversation flow

### Key Architecture Files

**Core System Components**
- `app.py` - Main Flask application with voice processing endpoints
- `utils/crew_agents.py` - MultiAgentConversationOrchestrator using CrewAI
- `utils/persona_system.py` - Persona definitions and management
- `utils/groq_integration.py` - LLM response generation
- `utils/groq_transcribe.py` - Speech-to-text processing
- `utils/groq_tts_speech.py` - Text-to-speech generation
- `utils/database.py` - SQLite conversation persistence
- `static/js/main.js` - Frontend voice processing and agent interaction