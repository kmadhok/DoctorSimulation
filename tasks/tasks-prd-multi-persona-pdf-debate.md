# Tasks: Multi-Persona PDF Debate System

## Relevant Files

- `DoctorSimulation/utils/persona_system.py` - ✅ MODIFIED: Replaced medical personas with debate personas (Hope, Sage, Alex)
- `DoctorSimulation/test_multi_agent_mock.py` - ✅ MODIFIED: Updated for debate personas and personality checks
- `DoctorSimulation/utils/crew_agents.py` - Multi-agent orchestrator that needs enhancement for autonomous debates
- `DoctorSimulation/utils/pdf_processor.py` - New file for PDF text extraction and processing (to be created)
- `DoctorSimulation/utils/database.py` - Existing database module that needs extension for PDF content storage
- `DoctorSimulation/app.py` - Main Flask app requiring new PDF upload endpoints and enhanced multi-agent routes
- `DoctorSimulation/templates/index.html` - Frontend template needing PDF upload component and debate controls
- `DoctorSimulation/static/js/main.js` - Frontend JavaScript requiring PDF upload and debate management functionality
- `DoctorSimulation/static/css/style.css` - Styling for new PDF upload and debate interface components
- `tests/test_pdf_processor.py` - Unit tests for PDF processing functionality (to be created)
- `tests/test_debate_personas.py` - ✅ CREATED: Unit tests for debate persona system with 9 comprehensive validation tests
- `tests/test_pdf_integration.py` - Integration tests for PDF-based conversations (to be created)

### Notes

- PDF processing libraries (pdfplumber, pypdfium2) are already in requirements.txt
- Multi-agent orchestrator and voice processing infrastructure is already implemented
- Database and conversation management systems are established and just need extension

## Tasks

- [ ] 1.0 Replace Medical Personas with Debate Personas System
  - [x] 1.1 Define three new debate personas (Optimistic, Negative, Neutral) with distinct personality traits, speaking styles, and debate behaviors
  - [x] 1.2 Update `PERSONAS` dictionary in `utils/persona_system.py` to replace medical personas with debate personas
  - [x] 1.3 Create debate-focused prompt templates that encourage argumentation, perspective-taking, and referencing source material
  - [x] 1.4 Assign distinct voice IDs for each debate persona (enthusiastic voice for Optimistic, cautious voice for Negative, steady voice for Neutral)
  - [x] 1.5 Add debate-specific response patterns (challenge opposing views, support arguments with evidence, acknowledge counterpoints)
  - [x] 1.6 Test persona responses to ensure distinct personalities and debate behaviors are working correctly

- [ ] 2.0 Implement PDF Upload and Processing Infr  astructure
  - [ ] 2.1 Create `utils/pdf_processor.py` emodule with functions for PDF text extraction using pdfplumber library
  - [ ] 2.2 Add PDF file validation (format checking, size limits ≤5 pages, malicious content scanning)
  - [ ] 2.3 Implement text extraction with error handling for corrupted or image-heavy PDFs
  - [ ] 2.4 Add `store_pdf_content()` and `get_pdf_content()` functions to `utils/database.py` for conversation-linked storage
  - [ ] 2.5 Create `/api/upload-pdf` Flask endpoint in `app.py` for handling file uploads with proper error responses
  - [ ] 2.6 Add database schema extension to store PDF content, filename, and processing metadata
  - [ ] 2.7 Implement PDF content chunking for large documents to optimize AI context window usage
  - [ ] 2.8 Add comprehensive error handling and logging for PDF processing failures

- [ ] 3.0 Enhance Multi-Agent Orchestrator for Autonomous Debates
  - [ ] 3.1 Modify `MultiAgentConversationOrchestrator` in `crew_agents.py` to include PDF content in agent context
  - [ ] 3.2 Add `debate_mode` parameter to orchestrator initialization for debate-specific behavior
  - [ ] 3.3 Implement enhanced `_moderator_pick()` function that encourages back-and-forth debates between opposing personas
  - [ ] 3.4 Add `inject_pdf_context()` method to provide all agents access to PDF content and key discussion points
  - [ ] 3.5 Create debate-specific prompt engineering that encourages agents to reference PDF content and challenge each other's interpretations
  - [ ] 3.6 Enhance `generate_auto_turn()` function to create longer debate sequences (3-4 exchanges) without user input
  - [ ] 3.7 Add debate topic extraction from PDF content to seed initial discussion points
  - [ ] 3.8 Implement conflict resolution logic when personas have strongly opposing interpretations

- [ ] 4.0 Build Frontend PDF Upload and Debate Interface
  - [ ] 4.1 Add PDF upload component to `templates/index.html` with drag-and-drop functionality and file selection
  - [ ] 4.2 Create upload progress indicator and file validation feedback (file type, size, processing status)
  - [ ] 4.3 Add debate control panel with Start Debate, Pause, Continue, and Reset Discussion buttons
  - [ ] 4.4 Implement conversation status display showing current PDF title, processing status, and active debate personas
  - [ ] 4.5 Update `static/js/main.js` with PDF upload handling, file validation, and AJAX upload functionality
  - [ ] 4.6 Add JavaScript functions for debate controls (initiate debates, handle auto-turn sequences)
  - [ ] 4.7 Create visual speaking indicators to show which persona is currently speaking during debates
  - [ ] 4.8 Style PDF upload and debate components in `static/css/style.css` with clear visual hierarchy
  - [ ] 4.9 Add responsive design support for mobile devices accessing the debate interface

- [ ] 5.0 Integrate PDF Content with Conversation Flow
  - [ ] 5.1 Modify conversation creation workflow to support PDF-based conversations with metadata storage
  - [ ] 5.2 Update `create_multi_agent_conversation()` endpoint to automatically initialize debate personas when PDF is uploaded
  - [ ] 5.3 Enhance `process_audio_multi_agent()` to inject PDF context into all agent responses
  - [ ] 5.4 Add PDF content summarization for conversation titles and metadata
  - [ ] 5.5 Implement conversation persistence that maintains PDF content across session loads
  - [ ] 5.6 Create `/api/pdf-conversation-summary` endpoint to provide debate highlights and key discussion points
  - [ ] 5.7 Add PDF content search functionality for agents to reference specific sections during debates
  - [ ] 5.8 Implement end-to-end testing workflow: PDF upload → persona initialization → debate conversation → conversation persistence
  - [ ] 5.9 Add conversation export functionality to save PDF debates as formatted transcripts 