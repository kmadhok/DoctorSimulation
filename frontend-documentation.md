# Frontend Documentation - Voice Conversation App

## Overview

This is a sophisticated voice conversation application that enables users to interact with AI personas through speech. The frontend is built as a single-page application (SPA) using vanilla JavaScript, HTML5, and CSS3, with Flask serving as the backend API provider.

## Architecture Overview

### Technology Stack

- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Audio Processing**: Web Audio API, MediaRecorder API
- **Voice Activity Detection**: Silero VAD model via ONNX Runtime
- **Real-time Communication**: WebRTC for audio capture
- **Backend Communication**: Fetch API for RESTful endpoints
- **UI Framework**: Custom CSS with responsive design

### Project Structure

```
├── templates/
│   └── index.html              # Main HTML template (Flask Jinja2)
├── static/
│   ├── js/
│   │   └── main.js            # Core JavaScript functionality (789 lines)
│   ├── css/
│   │   ├── style.css          # Main styles (2146 lines)
│   │   └── multi-agent.css    # Multi-agent specific styles (246 lines)
│   └── vad-model/             # Voice Activity Detection models
│       ├── ort.min.js         # ONNX Runtime
│       ├── bundle.min.js      # VAD bundle
│       └── *.onnx            # Pre-trained VAD models
├── app.py                     # Flask backend (2211 lines)
└── package.json              # Node.js dependencies for VAD
```

## Core Features

### 1. Voice Interaction System

#### Real-time Voice Activity Detection (VAD)
- **Implementation**: Uses Silero VAD model through ONNX Runtime
- **Purpose**: Automatically detects when user starts/stops speaking
- **Configuration**:
  ```javascript
  const myvad = await vad.MicVAD.new({
    positiveSpeechThreshold: 0.8,    // Sensitivity for speech start
    negativeSpeechThreshold: 0.5,     // Sensitivity for speech end
    preSpeechPadFrames: 8,           // Frames before speech
    minSpeechFrames: 3,              // Minimum frames for valid speech
    redemptionFrames: 10             // Frames to recover from false negative
  });
  ```

#### Audio Processing Pipeline
1. **Capture**: WebRTC getUserMedia API for microphone access
2. **Detection**: VAD determines speech boundaries
3. **Processing**: Convert Float32Array to WAV format
4. **Transmission**: Send audio blob to backend via FormData
5. **Response**: Receive transcription and AI response
6. **Playback**: Play TTS audio response through Web Audio API

### 2. Multi-Persona System

#### Persona Selection
```javascript
// Personas are loaded dynamically from backend
const response = await fetch('/api/personas');
const personas = response.json();
```

#### Persona Characteristics
- **Name and Description**: Identity and background
- **Voice ID**: TTS voice selection (PlayAI voices)
- **Personality Traits**: Behavioral characteristics
- **Speaking Style**: Communication patterns
- **Response Patterns**: Conversation approach

### 3. Multi-Agent Conference Calls

#### Agent Selection UI
- Modal-based interface for selecting multiple personas
- Dynamic agent list population
- Minimum 2 agents required for conference calls
- Real-time validation of selection

#### Conference Call Management
```javascript
// Start multi-agent conversation
const response = await fetch('/api/multi-agent/create', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ agent_ids: selectedAgents })
});
```

#### Multi-Agent Message Display
- Speaker labels for each agent response
- Distinct styling for different participants
- Sequential audio playback for multiple responses

### 4. Conversation Management

#### Conversation History
- **Storage**: SQLite database via Flask backend
- **Display**: Sidebar with conversation list
- **Features**: Load previous conversations, delete conversations, create new conversations

#### Real-time Updates
```javascript
// Auto-refresh conversation list
async function loadConversationHistory() {
  const response = await fetch('/api/conversations');
  const data = await response.json();
  populateConversationList(data.conversations);
}
```

### 5. Medical Case Generation (AI-Powered)

#### Dynamic Form System
- **Specialty Selection**: Medical specialties loaded from backend
- **Symptom Selection**: Dynamic symptom checkboxes based on specialty
- **Patient Demographics**: Age, gender, occupation inputs
- **Validation**: Real-time form validation with error display

#### Wizard Interface
- Multi-step form progression
- Progress indicators
- Form state management
- Preview of generated case

## Technical Implementation

### Audio System Architecture

#### Voice Activity Detection (VAD)
```javascript
// VAD initialization with error handling
async function initAutoVAD() {
  try {
    // Configure ONNX Runtime
    ort.env.wasm.wasmPaths = '/static/vad-model/';
    ort.env.wasm.numThreads = 1;
    ort.env.wasm.simd = true;
    
    const myvad = await vad.MicVAD.new({
      modelPath: '/static/vad-model/silero_vad_legacy.onnx',
      workletPath: '/static/vad-model/vad.worklet.bundle.min.js',
      onSpeechStart: () => { /* Handle speech start */ },
      onSpeechEnd: async (float32Audio) => { /* Process audio */ }
    });
    
    await myvad.start();
    return () => myvad.destroy(); // Cleanup function
  } catch (error) {
    // Fallback to manual recording
    showManualRecordingOption();
  }
}
```

#### Audio Format Conversion
```javascript
// Convert Float32Array to WAV format
function float32ToWav(float32, sampleRate = 16000) {
  const arrayBuffer = new ArrayBuffer(44 + float32.length * 2);
  const view = new DataView(arrayBuffer);
  
  // WAV header construction
  const writeString = (offset, string) => {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };
  
  writeString(0, 'RIFF');
  view.setUint32(4, 36 + float32.length * 2, true);
  writeString(8, 'WAVE');
  // ... additional WAV header setup
  
  return new Blob([arrayBuffer], { type: 'audio/wav' });
}
```

### State Management

#### Global State Variables
```javascript
// Conversation state
let currentConversationId = null;
let conversation_history = [];
let currentVoiceId = 'Fritz-PlayAI';

// Audio state
let stopVAD = null;
let audioContext;
let mediaRecorder = null;
let isRecording = false;

// Multi-agent state
let multiAgentMode = false;
let activeAgents = [];
let currentMultiAgentConversationId = null;

// Form state
let formState = {
  selectedSpecialty: null,
  selectedSymptoms: [],
  isLoading: false
};
```

#### State Synchronization
- Frontend state synced with backend via REST APIs
- Conversation data persisted in SQLite database
- Session management for maintaining user context

### API Integration

#### Backend Communication Patterns
```javascript
// Standard API call pattern
async function processAudio(audioBlob) {
  const formData = new FormData();
  formData.append('audio', audioBlob);
  formData.append('conversation_id', currentConversationId);
  
  const response = await fetch('/process_audio', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  if (data.status === 'success') {
    addMessage('user', data.user_transcription);
    addMessage('assistant', data.ai_response);
    await playAudioResponse(data.audio_response);
  }
}
```

#### Error Handling
- Graceful degradation for failed audio initialization
- Fallback to manual recording mode
- User-friendly error messages
- Retry mechanisms for network failures

### User Interface Components

#### Responsive Layout System
```css
/* Three-panel layout: Sidebar + Main + Diagnosis Panel */
.container.with-sidebar {
  display: flex;
  max-width: 1200px;
  gap: 2rem;
}

.container.with-sidebar.with-diagnosis {
  max-width: 1600px;
  gap: 1rem;
}

/* Mobile-first responsive design */
@media (max-width: 900px) {
  .container.with-sidebar {
    flex-direction: column;
  }
}
```

#### Interactive Elements
- **Record Buttons**: Visual feedback for recording state
- **Status Indicators**: Real-time status updates with color coding
- **Message Bubbles**: Distinct styling for user vs. assistant messages
- **Modal Dialogs**: Multi-agent setup and form wizards

### Performance Optimizations

#### Audio Queue Management
```javascript
let audioQueue = [];
let isAudioPlaying = false;

async function playAudioResponse(base64Audio) {
  audioQueue.push(base64Audio);
  if (!isAudioPlaying) {
    await processAudioQueue();
  }
}

async function processAudioQueue() {
  isAudioPlaying = true;
  while (audioQueue.length > 0) {
    const audioData = audioQueue.shift();
    await playAudioBlob(audioData);
  }
  isAudioPlaying = false;
}
```

#### Memory Management
- Proper cleanup of audio contexts
- VAD instance destruction on component unmount
- Blob URL cleanup after audio playback

### Accessibility Features

#### Keyboard Navigation
- Tab navigation for all interactive elements
- Enter/Space key support for buttons
- Focus management for modal dialogs

#### Screen Reader Support
- Semantic HTML structure
- ARIA labels for complex components
- Status announcements for dynamic content

#### Visual Indicators
- High contrast design
- Clear visual feedback for all states
- Responsive text scaling

## Integration Points

### Backend API Endpoints

#### Core Conversation API
- `POST /process_audio` - Process voice input
- `POST /process_audio_multi_agent` - Multi-agent voice processing
- `GET /api/conversations` - List conversations
- `POST /api/conversations/new` - Create new conversation
- `DELETE /api/conversations/<id>` - Delete conversation

#### Persona Management
- `GET /api/personas` - List available personas
- `POST /api/select-persona` - Select conversation persona
- `POST /api/update-voice` - Update voice settings

#### Multi-Agent Features
- `POST /api/multi-agent/create` - Create conference call
- `POST /api/multi-agent/add-agent` - Add agent to conversation
- `POST /api/multi-agent/process-message` - Process text message

#### Medical Case Generation
- `GET /api/medical-knowledge` - Get medical specialties/symptoms
- `POST /api/generate-patient-case` - Generate AI patient case
- `POST /api/create-custom-patient` - Create custom patient scenario

### Data Flow Architecture

#### User Input Flow
1. **Voice Input**: VAD detects speech → Audio captured → WAV conversion
2. **Backend Processing**: Audio sent to Flask → Groq transcription → AI response
3. **Response Handling**: Text response displayed → TTS audio generated → Audio playback

#### State Persistence Flow
1. **Local State**: JavaScript variables for immediate UI responsiveness
2. **Session State**: Backend session management for conversation context
3. **Database State**: SQLite storage for conversation history and user data

## Development Guidelines

### Code Organization
- **Modular Functions**: Single responsibility principle
- **Error Boundaries**: Try-catch blocks with graceful degradation
- **Async/Await**: Modern promise handling throughout
- **ES6+ Features**: Arrow functions, destructuring, template literals

### Debugging Features
- **VAD Logging**: Real-time debugging panel for voice detection
- **Console Logging**: Comprehensive logging for development
- **Error Reporting**: Detailed error messages with stack traces

### Testing Considerations
- **Audio System Testing**: Microphone permission handling
- **Cross-browser Compatibility**: Chrome, Firefox, Safari support
- **Mobile Responsiveness**: Touch-friendly interface design

## Future Enhancement Opportunities

### Performance Improvements
- Service Worker implementation for offline functionality
- WebAssembly optimization for audio processing
- Progressive Web App (PWA) features

### Feature Expansions
- Video call integration with WebRTC
- Real-time collaboration features
- Advanced voice customization options
- Integration with external medical databases

### Accessibility Enhancements
- Voice-only navigation mode
- Multiple language support
- Customizable UI themes
- Enhanced screen reader integration

This frontend architecture provides a robust foundation for voice-enabled AI conversations with extensibility for future enhancements while maintaining high performance and user experience standards.