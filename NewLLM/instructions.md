Specification: Voice Conversation Web Application (with Integrated Testing)

1. Goal: (Same as before)

Transform the existing Python voice conversation script (app.py and its dependencies) into a web application using the Flask framework.

Enable users to interact with the application via voice through their web browser's microphone.

Maintain the core conversation flow: User speaks -> Transcribe -> Get LLM response -> Synthesize response -> Play response -> Repeat.

Properly separate client-side (browser) tasks from server-side (Flask) tasks.

2. Current State: (Same as before)

A set of Python scripts (app.py, groq_integration.py, groq_transcribe.py, groq_tts_speech.py).

Direct use of sounddevice, Groq APIs, and pydub for playback in a single script execution context.

In-memory history management within app.py.

3. Target Architecture: (Same as before)

Backend: Flask application (Python)

Frontend: Web Browser (HTML, CSS, JavaScript)

4. Testing Strategy Overview:

Unit Tests: Use pytest (or Python's unittest) for testing isolated Python functions (especially helper modules), mocking external API calls.

Integration Tests: Test the interaction between Flask routes and helper functions. Can involve tools like pytest-flask and potentially controlled calls to actual APIs (use with caution/mocking). Test API endpoints using tools like curl, Postman, or Python's requests library.

Frontend Tests: Basic checks can be done via browser developer tools (Console, Network tabs). More advanced testing could use frameworks like Jest (for JS logic) or E2E tools like Selenium/Playwright/Cypress (more complex setup).

Manual Tests: Essential for verifying user experience, UI appearance, microphone access prompts, and actual audio input/output quality.

5. Core Requirements & Implementation Steps (with Testing):

Step 1: Project Setup

Action: Create Flask project structure (app.py, requirements.txt, .env, templates/index.html, static/js/main.js, static/css/style.css).

Action: Install Flask, Groq SDK, python-dotenv, pydub (if needed), numpy. List them in requirements.txt.

Action: Set up basic .env file for GROQ_API_KEY.

Testing:

[Manual] Verify requirements.txt accurately reflects necessary packages. Run pip install -r requirements.txt in a clean environment to confirm installation.

[Manual] Verify the basic project structure is created correctly.

[Manual] Ensure .env is correctly formatted (e.g., GROQ_API_KEY=your_key_here). Add .env to .gitignore.

Step 2: Flask Backend Foundation

Action: Set up a minimal Flask app in app.py that initializes the Flask object.

Action: Implement loading of GROQ_API_KEY from .env using dotenv.

Action: Create the / route serving a basic templates/index.html (e.g., just showing "Hello World").

Action: Create a stub for the /process_audio POST route that initially returns a simple placeholder JSON response (e.g., {'status': 'received'}).

Action: Implement basic server-side history management (start with a simple global list or dictionary). Add placeholder logic to update history in the stubbed /process_audio.

Testing:

[Integration] Run flask run (or python app.py). Verify the development server starts without errors.

[Integration] Access / in a web browser. Verify the "Hello World" (or basic content) from index.html is displayed.

[Integration] Use curl or Postman to send a POST request to /process_audio. Verify the placeholder JSON response is received (e.g., curl -X POST http://127.0.0.1:5000/process_audio).

[Unit/Integration] Write a test (using pytest or similar) to check if the API key is loaded correctly from the environment (can be tested by checking if app.config or a global variable is populated, might need mocking of os.getenv).

[Manual] Check server logs for any errors during startup or request handling.

Step 3: Refactor Helper Modules for Server Use

Action (groq_transcribe.py): Create a function transcribe_audio_data(audio_bytes, model="...") that accepts audio bytes and returns the transcription text. This function should contain the logic for calling the Groq API using the provided bytes (potentially saving them to a temporary file within the function if the Groq SDK requires a file path). Remove direct sounddevice calls from this function.

Action (groq_tts_speech.py): Create/modify a function generate_speech_audio(text, voice_id="...") that accepts text and returns the synthesized audio bytes (e.g., WAV format). Remove pydub.playback.play and os.remove (temporary file handling should be managed carefully or avoided if bytes can be handled directly).

Action (groq_integration.py): Ensure get_groq_response works correctly when called from Flask, especially regarding history management.

Testing:

[Unit] Write pytest unit tests for transcribe_audio_data. Use a sample audio file (e.g., a short WAV), read its bytes, and pass them to the function. Mock the Groq client's audio.transcriptions.create method to return a predefined response. Verify the function returns the expected text. Test edge cases (e.g., empty audio bytes).

[Unit] Write pytest unit tests for generate_speech_audio. Mock the Groq client's audio.speech.create method to simulate returning audio data (e.g., mock the write_to_file method or the response object itself). Verify the function returns non-empty bytes.

[Unit] Write pytest unit tests for get_groq_response. Mock the Groq client's chat.completions.create method. Test with and without history provided. Verify the correct message structure is passed to the mock and the expected response content is returned.

Step 4: Implement Backend API Logic (/process_audio)

Action: Update the /process_audio route to:

Receive an audio file/blob from the request (request.files).

Read the audio data bytes.

Call transcribe_audio_data with the bytes.

Implement the original script's logic: check for "exit"/"quit", check for repetition against llm_history.

Call get_groq_response with the transcription and current history.

Call generate_speech_audio with the LLM response text.

Base64 encode the returned audio bytes.

Update the server-side history list/dictionary.

Return a JSON response containing user_transcription, assistant_response_text, assistant_response_audio (base64 encoded), and status.

Testing:

[Integration] Use curl or Postman to POST a sample audio file (e.g., a WAV file) to /process_audio.

curl -X POST -F "audio=@path/to/your/sample.wav" http://127.0.0.1:5000/process_audio

[Integration] Verify the JSON response structure is correct and contains the expected keys.

[Integration] Verify the assistant_response_audio field contains a valid base64 string.

[Integration] (Optional/Advanced) Decode the received base64 audio data and manually verify it's playable audio (or automate this check if feasible).

[Integration] Send subsequent requests and verify that history is being accumulated and used (check server logs or add a debug endpoint to view history).

[Integration] Test the "exit"/"quit" logic by sending audio containing those words. Verify the response indicates termination.

[Integration] Test the repetition logic.

[Integration] Test error handling: Send a request with no file, or with a non-audio file. Verify appropriate error responses (e.g., 400 Bad Request) or error messages in the JSON.

[Manual] Monitor server logs during tests for uncaught exceptions or errors from the helper modules/API calls.

Step 5: Frontend HTML Structure (templates/index.html)

Action: Add necessary HTML elements: Record button, conversation display <div>, status indicator <span> or <p>.

Action: Include <script> tag for static/js/main.js and <link> tag for static/css/style.css.

Testing:

[Manual] Load the / route in a browser. Verify all UI elements (button, text areas) are present and visually acceptable (basic layout).

[Manual] Check the browser's developer console for any errors related to loading CSS or JS files (e.g., 404 Not Found).

Step 6: Frontend JavaScript Logic (static/js/main.js)

Action: Add event listener to the record button (e.g., mousedown/mouseup or click).

Action: Implement microphone access using navigator.mediaDevices.getUserMedia. Handle success and error cases (permissions denied).

Action: Implement audio recording using MediaRecorder. Start recording on button press, stop on release/timeout. Collect audio chunks into a Blob. Specify MIME type (e.g., audio/wav if possible, or audio/webm).

Action: Implement fetch POST request to /process_audio. Create FormData, append the audio Blob.

Action: Handle the JSON response from the backend: parse it, update the conversation display area with user transcription and assistant text.

Action: Implement audio playback: Take the base64 assistant_response_audio, decode it, create an ArrayBuffer, and use AudioContext.decodeAudioData and AudioBufferSourceNode to play it.

Action: Update the status indicator throughout the process ("Listening...", "Processing...", "Speaking...", "Error...").

Testing:

[Manual] Load the page. Click the record button. Verify the browser prompts for microphone permission. Grant permission.

[Manual] Click/hold the button again. Verify the status changes to "Listening...". Speak a phrase. Release the button.

[Manual] Check the browser's Developer Console (Network Tab): Verify a POST request is sent to /process_audio with audio data payload. Verify the JSON response is received.

[Manual] Verify the Developer Console (Console Tab) for any JavaScript errors during recording, sending, receiving, or playback.

[Manual] Verify the UI updates: Status changes ("Processing...", "Speaking..."), transcription appears, assistant text appears.

[Manual] Verify the assistant's audio response is played back through the speakers/headphones.

[Manual] Test denying microphone permission. Verify a user-friendly error message or state is shown.

[Manual] Test potential network errors (e.g., stop the Flask server and try recording). Verify error handling in the UI.

[E2E - Advanced] Use browser automation tools to script the button click, potentially mock getUserMedia, check network requests, and verify UI text updates. Automating audio playback verification is generally difficult.

7. Final End-to-End Testing:

Action: Perform several full conversation turns, simulating a natural interaction.

Testing:

[Manual] Verify the conversation flows logically and history is maintained correctly across turns.

[Manual] Check for latency issues (time between finishing speaking and hearing the response).

[Manual] Test edge cases like speaking very short phrases, long phrases, or silence.

[Manual] Verify the "exit"/"quit" commands successfully terminate the interaction flow (or trigger the appropriate backend response).

[Manual] Test in different supported browsers (if applicable, e.g., Chrome, Firefox).