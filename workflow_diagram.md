# Voice Conversation Web Application - Workflow Diagram

## Overview
This is a Flask-based voice conversation web application with medical simulation capabilities, multi-agent conversations, and AI-powered persona interactions.

---

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (Browser)     │◄──►│   (Flask)       │◄──►│   Services      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
│                      │                      │
├─ HTML/CSS/JS        ├─ Flask Routes         ├─ Groq API (LLM)
├─ VAD (Voice Detect) ├─ Database (SQLite)    ├─ Groq Whisper (STT)
├─ MediaRecorder API  ├─ Multi-Agent System   └─ Groq TTS (Speech)
└─ AudioContext       └─ Persona System
```

---

## 🔄 Core Workflow: Voice Conversation

### 1. Voice Input Processing
```
User Speaks
    ↓
[VAD Detection] ──→ Speech Start/End Events
    ↓
[MediaRecorder] ──→ Capture Audio (WebM/WAV)
    ↓
[Float32 to WAV] ──→ Convert Audio Format
    ↓
[POST /process_audio] ──→ Send to Backend
```

### 2. Backend Processing Pipeline
```
Audio Blob Received
    ↓
[groq_transcribe.py] ──→ Speech-to-Text via Groq Whisper
    ↓                      (transcribe_audio_data)
[Conversation History] ──→ Load Previous Messages
    ↓
[Persona System] ──→ Get Current Persona Prompt
    ↓
[groq_integration.py] ──→ Generate LLM Response
    ↓                     (get_groq_response)
[groq_tts_speech.py] ──→ Text-to-Speech via Groq TTS
    ↓                    (generate_speech_audio)
[Database Storage] ──→ Save Message to SQLite
    ↓
JSON Response ──→ Return to Frontend
```

### 3. Frontend Response Handling
```
JSON Response Received
    ↓
[UI Update] ──→ Display User & Assistant Messages
    ↓
[Base64 Decode] ──→ Convert Audio Data
    ↓
[AudioContext] ──→ Play TTS Response
    ↓
[Status Update] ──→ Ready for Next Input
```

---

## 👥 Multi-Agent Conference Call Workflow

### Setup Phase
```
User Clicks "Start Conference Call"
    ↓
[GET /api/personas] ──→ Load Available Personas
    ↓
[Agent Selection UI] ──→ User Selects 2+ Agents
    ↓
[POST /api/multi-agent/create] ──→ Initialize Multi-Agent System
    ↓
[MultiAgentConversationOrchestrator] ──→ Create Crew Agents
```

### Conversation Phase
```
User Speaks
    ↓
[VAD/Manual Recording] ──→ Capture Audio
    ↓
[POST /process_audio_multi_agent] ──→ Send to Multi-Agent Endpoint
    ↓
[Floor Manager LLM] ──→ Decide Which Agents Respond
    ↓
[Agent Response Generation] ──→ Each Agent Gets Context & Responds
    ↓
[Sequential Audio Playback] ──→ Play Each Agent's Response
```

### Multi-Agent Response Generation
```
User Message Input
    ↓
[Conversation Context] ──→ Get Recent 6-8 Messages
    ↓
[Agent Selection Logic] ──→ Floor Manager or Rotation
    ↓
For Each Selected Agent:
    ├─ [Persona Data] ──→ Load Character Traits
    ├─ [Context Prompt] ──→ Build Personality-Aware Prompt
    ├─ [LLM Call] ──→ Generate Individual Response
    └─ [TTS Generation] ──→ Create Audio for Agent's Voice
    ↓
[Response Queue] ──→ Return All Agent Responses
```

---

## 🏥 Medical Simulation Workflow

### AI Patient Case Generation
```
User Selects Medical Specialty
    ↓
[GET /api/medical-knowledge] ──→ Load Specialty Symptoms
    ↓
[User Symptom Selection] ──→ Choose Relevant Symptoms
    ↓
[POST /api/generate-patient-case] ──→ AI Generates Patient
    ↓
[ai_case_generator.py] ──→ Create Detailed Medical Case
    ↓
[Patient Data Storage] ──→ Store in Database
    ↓
[Conversation Initialization] ──→ Start Medical Interview
```

### Custom Patient Creation
```
User Inputs Patient Details
    ↓
[Form Validation] ──→ Validate Required Fields
    ↓
[POST /api/create-custom-patient] ──→ Create Custom Case
    ↓
[Database Storage] ──→ Store Patient Configuration
    ↓
[Persona Assignment] ──→ Set Patient Voice & Behavior
```

### Medical Interview Simulation
```
Doctor (User) Asks Question
    ↓
[Voice Processing] ──→ Standard Audio Pipeline
    ↓
[Patient Persona] ──→ Role-play as Specific Patient
    ↓
[Medical Context] ──→ Answer Based on Patient History
    ↓
[Diagnosis Panel] ──→ Track Interview Progress
```

---

## 🎭 Persona System Architecture

### Persona Structure
```
persona_system.py
    ├─ Persona Definitions (JSON-like)
    ├─ Character Traits
    ├─ Speaking Styles
    ├─ Response Patterns
    └─ Voice Assignments

Each Persona Contains:
    ├─ name: Display name
    ├─ description: Brief character description
    ├─ voice_id: TTS voice assignment
    └─ characteristics:
        ├─ personality_traits: []
        ├─ speaking_style: ""
        ├─ background: ""
        ├─ worldview: ""
        └─ response_patterns: []
```

### Persona Selection Flow
```
[GET /api/personas] ──→ List Available Personas
    ↓
[User Selection] ──→ Choose Persona
    ↓
[POST /api/select-persona] ──→ Set Active Persona
    ↓
[Database Storage] ──→ Store Selection
    ↓
[System Prompt Update] ──→ Apply Persona Characteristics
```

---

## 💾 Database Schema & Data Flow

### Tables Structure
```
conversations
    ├─ id (Primary Key)
    ├─ title
    ├─ simulation_file
    ├─ created_at
    └─ updated_at

messages
    ├─ id (Primary Key)
    ├─ conversation_id (Foreign Key)
    ├─ role (user/assistant)
    ├─ content
    └─ timestamp

conversation_data
    ├─ id (Primary Key)
    ├─ conversation_id (Foreign Key)
    ├─ data_key
    ├─ data_value (JSON)
    ├─ data_type
    ├─ created_at
    └─ updated_at
```

### Data Storage Patterns
```
Conversation Metadata:
    ├─ persona_data: Selected persona information
    ├─ voice_id: TTS voice selection
    ├─ patient_data: Medical simulation data
    ├─ conversation_type: single/multi_agent
    └─ active_agents: Multi-agent participant list

Patient Data Structure:
    ├─ type: ai_generated/custom/file_based
    ├─ prompt_template: Patient behavior instructions
    ├─ patient_details: Medical history & symptoms
    ├─ voice_id: Patient voice selection
    └─ metadata: Generation/creation details
```

---

## 🎮 Frontend User Interface Flow

### Main Interface States
```
1. Initial State
    ├─ Persona Selection
    ├─ Voice Selection
    └─ Conversation History Sidebar

2. Active Conversation
    ├─ Voice Detection (Auto/Manual)
    ├─ Status Display
    ├─ Message Display
    └─ Audio Playback

3. Multi-Agent Mode
    ├─ Agent Selection Panel
    ├─ Conference Call Indicator
    ├─ Multiple Speaker Labels
    └─ Sequential Audio Playback

4. Medical Simulation
    ├─ Specialty Selection
    ├─ Symptom Configuration
    ├─ Patient Case Display
    └─ Diagnosis Panel
```

### Client-Side Audio Processing
```
Voice Activity Detection (VAD)
    ├─ ONNX Runtime Integration
    ├─ Silero VAD Model
    ├─ Real-time Speech Detection
    └─ Audio Chunk Processing

Audio Recording
    ├─ MediaRecorder API
    ├─ Float32 Audio Conversion
    ├─ WAV Format Generation
    └─ Blob Creation

Audio Playback
    ├─ Base64 Decode
    ├─ AudioContext
    ├─ Buffer Management
    └─ Queue Processing
```

---

## 🔌 API Endpoints Overview

### Core Conversation
- `GET /` - Main interface
- `POST /process_audio` - Single agent audio processing
- `POST /process_audio_multi_agent` - Multi-agent audio processing

### Persona Management
- `GET /api/personas` - List available personas
- `POST /api/select-persona` - Select conversation persona
- `POST /api/update-voice` - Change TTS voice

### Multi-Agent System
- `POST /api/multi-agent/create` - Create multi-agent conversation
- `POST /api/multi-agent/add-agent` - Add agent to conversation
- `POST /api/multi-agent/process-message` - Process text message

### Medical Simulation
- `GET /api/medical-knowledge` - Get medical specialties/symptoms
- `POST /api/generate-patient-case` - Generate AI patient
- `POST /api/create-custom-patient` - Create custom patient
- `POST /api/submit-diagnosis` - Submit medical diagnosis

### Conversation Management
- `GET /api/conversations` - List conversation history
- `POST /api/conversations/new` - Create new conversation
- `GET /api/conversations/<id>` - Get specific conversation
- `DELETE /api/conversations/<id>` - Delete conversation
- `POST /api/conversations/<id>/load` - Load conversation

---

## 🔄 Error Handling & Fallbacks

### Audio System Fallbacks
```
VAD Initialization Failure
    ↓
[Error Detection] ──→ Log Error Details
    ↓
[Manual Mode Activation] ──→ Show Manual Recording Button
    ↓
[User Notification] ──→ Update Status Message
```

### API Error Handling
```
Groq API Failure
    ↓
[Error Logging] ──→ Log to app.log
    ↓
[User Feedback] ──→ Display Error Message
    ↓
[Graceful Degradation] ──→ Maintain Conversation State
```

### Database Error Recovery
```
Database Connection Issues
    ↓
[Retry Logic] ──→ Attempt Reconnection
    ↓
[Migration Handling] ──→ Apply Schema Updates
    ↓
[Backup/Restore] ──→ Data Recovery Options
```

---

## 🚀 Key Features Summary

1. **Voice-First Interface**: Hands-free conversation with VAD
2. **Multi-Agent Conversations**: Multiple AI personas in group chats
3. **Medical Training**: AI-generated patient cases for medical education
4. **Flexible Personas**: Customizable AI personalities and voices
5. **Conversation Persistence**: Full conversation history with database storage
6. **Real-time Audio**: Low-latency speech recognition and synthesis
7. **Responsive UI**: Modern web interface with sidebar navigation
8. **Error Recovery**: Robust fallback mechanisms for audio/network issues

---

## 🔧 Technical Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with migration support
- **AI Services**: Groq (LLM, STT, TTS)
- **Frontend**: Vanilla JavaScript with VAD
- **Audio Processing**: MediaRecorder API, AudioContext, ONNX Runtime
- **Multi-Agent**: CrewAI framework integration
- **Voice Detection**: Silero VAD model