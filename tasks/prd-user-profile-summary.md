# Product Requirements Document: User Profile Summary Box

## Introduction/Overview

This feature adds a user profile summary box to the conversation interface that analyzes user behavior patterns and emotional trends across all conversations. The summary box will be displayed as an always-visible sidebar panel that helps users understand their own conversation patterns and personal growth over time.

The feature addresses the need for users to gain insights into their communication styles, emotional patterns, and personality traits as revealed through their conversations with different AI personas.

## Goals

1. **Personal Insight**: Provide users with meaningful insights into their communication patterns and emotional tendencies
2. **Self-Awareness**: Help users understand their personality traits and how they interact with different personas
3. **Growth Tracking**: Enable users to see their emotional and conversational evolution over time
4. **User Control**: Allow users to modify the displayed summary to reflect their own perspective

## User Stories

1. **As a user**, I want to see a summary of my personality and emotional patterns so that I can better understand myself through my conversations.

2. **As a user**, I want to view insights from all my conversations across different personas so that I can see how I interact differently with various personality types.

3. **As a user**, I want to edit the summary text so that it accurately reflects my perspective and self-understanding.

4. **As a user**, I want the summary to update when I request it so that I can see fresh insights after having more conversations.

5. **As a new user**, I want to see a helpful message when I don't have enough conversations yet so that I understand when the feature will become available.

## Functional Requirements

1. **Data Collection**: The system must analyze all user messages from conversations stored in the conversations.db database.

2. **Minimum Threshold**: The system must require a minimum of 5 completed conversations before generating a profile summary.

3. **Emotional Analysis**: The system must use LLM analysis to identify emotional patterns and mood trends from user transcripts.

4. **Always-Visible Display**: The summary must be displayed in an always-visible sidebar panel in the main conversation interface.

5. **User Editing**: Users must be able to modify the displayed summary text to reflect their own perspective.

6. **On-Demand Updates**: The system must provide a refresh mechanism that allows users to request updated analysis.

7. **Cross-Persona Analysis**: The system must analyze conversations across all personas, not just the currently selected one.

8. **Error Handling**: The system must handle brief conversations by summarizing available content and display "not available currently" for database or LLM API failures.

9. **Graceful Degradation**: For new users with insufficient conversation history, the system must display an informative message about the minimum requirement.

## Non-Goals (Out of Scope)

1. **Real-time Updates**: The summary will not update automatically after each message
2. **Historical Tracking**: The system will not maintain a timeline of how summaries change over time
3. **Persona-Specific Analysis**: The system will not provide separate summaries for each persona
4. **Advanced Analytics**: No charts, graphs, or detailed metrics beyond text summary
5. **Data Export**: Users cannot export or download their profile data
6. **Privacy Controls**: Beyond text editing, no granular privacy controls for specific conversations

## Design Considerations

- **Sidebar Layout**: Always-visible panel positioned to the right of the conversation messages
- **Editable Interface**: Text area or contenteditable div allowing users to modify summary
- **Loading States**: Clear visual indicators during summary generation
- **Error States**: Friendly error messages for various failure scenarios
- **Responsive Design**: Summary panel should adapt to different screen sizes
- **Refresh Button**: Clear UI element for requesting updated analysis

## Technical Considerations

- **Database Integration**: Leverage existing SQLite conversations.db structure
- **LLM Integration**: Use existing Groq API integration for analysis
- **Frontend Integration**: Extend existing static/js/main.js and templates/index.html
- **API Design**: RESTful endpoints following existing Flask application patterns
- **Error Handling**: Consistent with existing application error handling patterns
- **Performance**: Real-time database queries acceptable given typical conversation volumes

## Success Metrics

1. **Primary Success**: Successful display of user personality and emotional insights for users with sufficient conversation history
2. **User Engagement**: Users actively read and interact with their profile summary
3. **Feature Adoption**: Users with 5+ conversations successfully see generated summaries
4. **Error Handling**: Graceful handling of edge cases without application crashes
5. **User Satisfaction**: Users find the summary accurate and insightful (qualitative feedback)

## Open Questions

1. **Performance Optimization**: Should we implement caching for frequently accessed summaries?
2. **Summary Length**: What is the optimal length for user profile summaries?
3. **Update Frequency**: Should we set limits on how often users can refresh their summary?
4. **Conversation Filtering**: Should users be able to exclude specific conversations from analysis?
5. **Mobile Experience**: How should the always-visible sidebar adapt for mobile devices?