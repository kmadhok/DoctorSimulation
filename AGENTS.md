# AGENTS.md

## Cursor Cloud specific instructions

This repo is a single Flask web app ("Voice Conversation App" / doctor–patient
simulation): the browser records audio, and the server transcribes it, gets an
LLM reply, and returns synthesized speech via the **Groq API**. State is stored
in a local SQLite file (`conversations.db`). See `README.md` and `instructions.md`
for the product spec.

Python deps are installed into a virtualenv at `.venv` by the startup update
script. Always use `.venv/bin/python` / `.venv/bin/pytest` (not the system
Python). `python3.12-venv` (system apt package) is required to create the venv.

### Running the app (IMPORTANT gotcha)
- Do **NOT** run `python app.py`. In `app.py` the `if __name__ == '__main__'`
  block (which calls `app.run()`) is defined *before* the `@app.route`
  decorators, so running the file directly starts a server with **no routes
  registered** — every URL returns 404.
- Run the app by importing the module instead:
  - Dev: `.venv/bin/flask --app app run --host 0.0.0.0 --port 5000`
  - Prod-style (as in `Procfile`): `.venv/bin/gunicorn app:app`
- The app serves on port 5000.

### Groq API key
- The full voice loop (Whisper transcription, `llama3-8b-8192` chat, `playai-tts`)
  requires a valid `GROQ_API_KEY` env var (read by `utils/groq_transcribe.py` and
  `utils/groq_tts_speech.py`). `utils/groq_integration.py` has a hardcoded key that
  is **invalid (returns HTTP 401)** — set a real `GROQ_API_KEY` to exercise any
  Groq-powered flow. Outbound HTTPS to `api.groq.com` works from the VM.
- `groq==0.4.0` requires `httpx<0.28` (pinned in `requirements.txt`); newer httpx
  removed the `proxies` kwarg and breaks the Groq client.

### Patient simulations
- The simulation dropdown is empty by default: `app.py` globs
  `patient_simulation_*.json` in the repo root, but the sample files live under
  `prompts/results/`. To select one, POST an explicit path to
  `/api/select-simulation`, pass `--patient-file <path>`, or copy a file to root.

### Tests / lint
- Canonical entrypoint: `./run_tests.sh` (runs `pytest tests/test_audio_recording.py`
  then `npm test`). The Python target (6 tests) passes.
- `npm test` reports "No tests found": Jest's default `testMatch` doesn't match the
  `tests/test_*.js` naming. Run the JS suite explicitly with
  `npx jest --testMatch='**/tests/test_audio_recording.js'`.
- Several other test modules are **pre-existing failures** unrelated to
  environment setup (they reference modules/classes that don't exist or use
  outdated mocks): `tests/test_environment.py` (`utils.environment` missing),
  `tests/test_patient_simulation.py` (`PatientSimulator` missing), and assertion
  mismatches in `test_app.py`, `test_database.py`, `test_groq_integration.py`,
  `test_transcription.py`, `test_tts.py`, plus the forced JS tests.
- No linter is configured in this repo.
