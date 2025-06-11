# Branch Description

custom_v2: Able to set a custom prompt and interact with that custom prompt/patient without issue.



# Voice Conversation Web Application

A web-based voice conversation application that uses Groq APIs for transcription, language model responses, and text-to-speech.

## Features

- Record voice using the browser's microphone
- Transcribe speech to text using Groq's Whisper API
- Generate responses using Groq's LLM API
- Convert responses to speech using Groq's TTS API
- Maintain conversation history

## Prerequisites

- Python 3.8+
- Groq API key (get one from [Groq Console](https://console.groq.com/keys))

## Setup

1. Clone this repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Create a `.env` file with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```
4. Run the application:
```
python app.py
```
5. Open your browser and go to `http://127.0.0.1:5000`

## Usage

1. Click and hold the "Hold to Speak" button
2. Speak your message
3. Release the button to process your message
4. The application will transcribe your speech, get a response, and play it back

## Project Structure

- `app.py`: Main Flask application
- `utils/`: Helper modules
  - `groq_integration.py`: Functions for interacting with Groq LLM API
  - `groq_transcribe.py`: Functions for transcribing speech using Groq API
  - `groq_tts_speech.py`: Functions for generating speech using Groq API
- `templates/`: HTML templates
  - `index.html`: Main page template
- `static/`: Static assets
  - `js/main.js`: Client-side JavaScript
  - `css/style.css`: Styling

## Testing

To test the application:

1. Manual testing: Verify the UI elements are present and working correctly
2. Integration testing: Use tools like curl or Postman to test the API endpoints
3. End-to-end testing: Perform full conversation flows to verify functionality

## License

MIT License 