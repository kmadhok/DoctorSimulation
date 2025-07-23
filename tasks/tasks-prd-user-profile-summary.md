# Task List: User Profile Summary Box

## Relevant Files

- `utils/user_profile_analyzer.py` - Core module for analyzing user conversations and generating personality insights
- `utils/user_profile_analyzer.test.py` - Unit tests for user profile analyzer
- `app.py` - Flask application routes for user profile API endpoints
- `templates/index.html` - Main template with user profile sidebar integration
- `static/js/main.js` - Frontend JavaScript for profile display and user interactions
- `static/css/style.css` - Styling for user profile sidebar and components
- `tests/test_user_profile_api.py` - Integration tests for user profile API endpoints
- `tests/unit/test_user_profile_analyzer.py` - Unit tests for profile analysis logic

### Notes

- Unit tests should be placed alongside the code files they are testing
- Use `python -m pytest [optional/path/to/test/file]` to run tests
- Integration tests go in the `tests/` directory following existing patterns

## Tasks

- [x] 1.0 Create User Profile Analysis Backend Module
  - [x] 1.1 Create `utils/user_profile_analyzer.py` with database query functions to retrieve all user messages from conversations.db
  - [x] 1.2 Create transcript aggregation function to combine user messages across all conversations
  - [x] 1.3 Design LLM prompt template for emotional pattern and personality analysis
  - [x] 1.4 Implement LLM integration using existing Groq API for personality analysis
  - [x] 1.5 Add error handling for brief conversations (summarize available content)
  - [x] 1.6 Add error handling for LLM API failures and database connection issues

- [ ] 2.0 Implement Flask API Endpoints for Profile Management
  - [x] 2.1 Create GET `/api/user-profile-summary` endpoint to generate/retrieve user profile analysis
  - [x] 2.2 Create PUT `/api/user-profile-summary` endpoint to save user-modified summary text
  - [x] 2.3 Integrate endpoints with existing Flask app structure in `app.py`
  - [x] 2.4 Add proper error responses for API failures (database, LLM, insufficient data)
  - [x] 2.5 Implement JSON response formatting consistent with existing API patterns

- [ ] 3.0 Build Frontend User Interface Components
  - [x] 3.1 Create CSS styles for always-visible sidebar panel in `static/css/style.css`
  - [x] 3.2 Design responsive layout that adapts to different screen sizes
  - [x] 3.3 Create editable text area component for user summary modifications
  - [x] 3.4 Add loading spinner and error message display components
  - [x] 3.5 Create refresh button for on-demand profile updates
  - [x] 3.6 Style components to match existing application design

- [ ] 4.0 Integrate Profile Summary with Main Conversation Interface
  - [ ] 4.1 Modify `templates/index.html` to include user profile sidebar section
  - [ ] 4.2 Update `static/js/main.js` to add profile summary functionality
  - [ ] 4.3 Implement API calls for profile generation and updates
  - [ ] 4.4 Add event handlers for user text editing and refresh button
  - [ ] 4.5 Implement conditional display logic (show summary only with 5+ conversations)
  - [ ] 4.6 Add error handling and user feedback for API failures
  - [ ] 4.7 Ensure profile summary loads on page initialization

- [ ] 5.0 Implement Testing and Error Handling
  - [ ] 5.1 Create unit tests for `user_profile_analyzer.py` functions
  - [ ] 5.2 Write integration tests for API endpoints in `tests/test_user_profile_api.py`
  - [ ] 5.3 Test edge cases: new users, insufficient conversations, brief conversations
  - [ ] 5.4 Test error scenarios: database failures, LLM API failures
  - [ ] 5.5 Create frontend tests for UI interactions and API integration
  - [ ] 5.6 Verify graceful degradation and appropriate error messages
  - [ ] 5.7 Test user editing functionality and data persistence