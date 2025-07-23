import sqlite3
import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Import existing Groq integration
try:
    from .groq_integration import get_groq_response
except ImportError:
    try:
        # For standalone testing
        from groq_integration import get_groq_response
    except ImportError:
        # Mock function for testing when Groq is not available
        def get_groq_response(input_text, model=None, history=None, system_prompt=None):
            return "Error: Groq API not available in test environment"

# Initialize logger
logger = logging.getLogger(__name__)

# Database file path - use same path as existing database module
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conversations.db')

# LLM prompt template for personality analysis
PERSONALITY_ANALYSIS_PROMPT = """You are an expert psychological analyst specializing in personality assessment through conversation analysis. Your task is to analyze user conversation transcripts and provide insights into their emotional patterns, communication style, and personality traits.

**ANALYSIS OBJECTIVES:**
1. Identify emotional patterns and mood trends across conversations
2. Determine communication style and preferences
3. Assess personality traits and characteristics
4. Note behavioral patterns and interpersonal dynamics
5. Observe growth or changes over time

**ANALYSIS FRAMEWORK:**
Analyze the following aspects:

- **Emotional Patterns**: Dominant emotions, emotional range, mood stability, emotional triggers
- **Communication Style**: Directness, formality, expressiveness, question-asking patterns, topic preferences
- **Personality Traits**: Extraversion/introversion, openness to experience, conscientiousness, agreeableness, neuroticism
- **Behavioral Patterns**: Problem-solving approach, response to different personas, conversation depth preferences
- **Interpersonal Dynamics**: How they interact with different personality types, relationship building style
- **Growth Indicators**: Changes in communication patterns, emotional development, increasing self-awareness

**OUTPUT FORMAT:**
Provide a comprehensive personality summary in the following structure:

## Personality Overview
[2-3 sentences summarizing the user's core personality]

## Emotional Patterns
[Describe emotional tendencies, mood patterns, and emotional intelligence indicators]

## Communication Style
[Detail how they express themselves, preferred communication methods, and conversation patterns]

## Key Personality Traits
[List 4-5 dominant personality traits with brief explanations]

## Behavioral Insights
[Describe problem-solving style, decision-making patterns, and interpersonal approach]

## Growth and Development
[Note any changes over time, areas of development, or evolving patterns]

**ANALYSIS GUIDELINES:**
- Base conclusions on observable patterns in the conversation data
- Avoid making assumptions beyond what the data supports
- Focus on constructive insights that could help user self-awareness
- Maintain a supportive, non-judgmental tone
- Highlight both strengths and areas for potential growth
- Consider context of different personas and conversation types
- Be specific with examples when possible (without repeating entire conversations)

**IMPORTANT CONSTRAINTS:**
- Only analyze what is explicitly present in the conversation data
- Avoid clinical diagnoses or medical assessments
- Focus on communication patterns and expressed thoughts/feelings
- Maintain respect for the user's privacy and dignity
- Provide balanced perspective highlighting both positive traits and growth areas

Now analyze the following conversation data:

{transcript_data}

Please provide your personality analysis following the format above."""

def create_personality_analysis_prompt(aggregated_transcripts: Dict) -> str:
    """
    Create a complete LLM prompt for personality analysis using aggregated transcript data.
    
    Args:
        aggregated_transcripts (Dict): Result from aggregate_user_transcripts()
        
    Returns:
        str: Complete prompt ready for LLM analysis
    """
    try:
        # Check if we have valid transcript data
        if aggregated_transcripts.get('status') != 'success':
            logger.error(f"Invalid transcript data for prompt creation: {aggregated_transcripts.get('message', 'Unknown error')}")
            return ""
        
        # Format the transcript data for analysis
        formatted_transcripts = format_transcripts_for_analysis(aggregated_transcripts)
        
        # Create the complete prompt
        complete_prompt = PERSONALITY_ANALYSIS_PROMPT.format(
            transcript_data=formatted_transcripts
        )
        
        logger.info(f"Created personality analysis prompt: {len(complete_prompt)} characters")
        return complete_prompt
        
    except Exception as e:
        logger.error(f"Error creating personality analysis prompt: {e}")
        return ""

def get_prompt_template() -> str:
    """
    Get the raw personality analysis prompt template.
    
    Returns:
        str: The prompt template with placeholder
    """
    return PERSONALITY_ANALYSIS_PROMPT

def validate_prompt_template() -> bool:
    """
    Validate that the prompt template is properly formatted and contains required elements.
    
    Returns:
        bool: True if template is valid, False otherwise
    """
    try:
        # Check if template exists and is not empty
        if not PERSONALITY_ANALYSIS_PROMPT or len(PERSONALITY_ANALYSIS_PROMPT.strip()) == 0:
            logger.error("Personality analysis prompt template is empty")
            return False
        
        # Check if required placeholder exists
        if '{transcript_data}' not in PERSONALITY_ANALYSIS_PROMPT:
            logger.error("Personality analysis prompt template missing {transcript_data} placeholder")
            return False
        
        # Check if required sections are present
        required_sections = [
            'ANALYSIS OBJECTIVES',
            'ANALYSIS FRAMEWORK',
            'OUTPUT FORMAT',
            'ANALYSIS GUIDELINES',
            'IMPORTANT CONSTRAINTS'
        ]
        
        for section in required_sections:
            if section not in PERSONALITY_ANALYSIS_PROMPT:
                logger.error(f"Personality analysis prompt template missing required section: {section}")
                return False
        
        # Check if output format sections are present
        output_sections = [
            'Personality Overview',
            'Emotional Patterns',
            'Communication Style',
            'Key Personality Traits',
            'Behavioral Insights',
            'Growth and Development'
        ]
        
        for section in output_sections:
            if section not in PERSONALITY_ANALYSIS_PROMPT:
                logger.error(f"Personality analysis prompt template missing output section: {section}")
                return False
        
        logger.debug("Personality analysis prompt template validation successful")
        return True
        
    except Exception as e:
        logger.error(f"Error validating prompt template: {e}")
        return False

def analyze_user_personality() -> Dict:
    """
    Analyze user personality using LLM based on aggregated conversation transcripts.
    
    Returns:
        Dict: Structured personality analysis results with metadata and error handling
    """
    try:
        logger.info("Starting user personality analysis...")
        
        # Step 1: Validate database connection
        if not validate_database_connection():
            logger.error("Database connection validation failed")
            return {
                'status': 'error',
                'error_type': 'database_connection',
                'message': 'Database connection failed. Please ensure the database is accessible.',
                'analysis': None,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'conversation_count': 0,
                    'analysis_successful': False
                }
            }
        
        # Step 2: Check minimum conversation requirement
        has_minimum, conversation_count = check_minimum_conversations()
        if not has_minimum:
            logger.warning(f"Insufficient conversations for personality analysis: {conversation_count}/5")
            return {
                'status': 'insufficient_data',
                'error_type': 'insufficient_conversations',
                'message': f'Need at least 5 conversations for personality analysis. Currently have {conversation_count}.',
                'analysis': None,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'conversation_count': conversation_count,
                    'analysis_successful': False
                }
            }
        
        # Step 3: Aggregate user transcripts
        logger.info("Aggregating user transcripts...")
        aggregated_transcripts = aggregate_user_transcripts()
        
        if aggregated_transcripts.get('status') != 'success':
            logger.error(f"Transcript aggregation failed: {aggregated_transcripts.get('message', 'Unknown error')}")
            return {
                'status': 'error',
                'error_type': 'transcript_aggregation',
                'message': f"Failed to aggregate conversation transcripts: {aggregated_transcripts.get('message', 'Unknown error')}",
                'analysis': None,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'conversation_count': conversation_count,
                    'analysis_successful': False
                }
            }
        
        # Step 4: Create personality analysis prompt
        logger.info("Creating personality analysis prompt...")
        complete_prompt = create_personality_analysis_prompt(aggregated_transcripts)
        
        if not complete_prompt:
            logger.error("Failed to create personality analysis prompt")
            return {
                'status': 'error',
                'error_type': 'prompt_creation',
                'message': 'Failed to create analysis prompt from conversation data.',
                'analysis': None,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'conversation_count': conversation_count,
                    'analysis_successful': False
                }
            }
        
        # Step 5: Call Groq API for personality analysis with enhanced error handling
        logger.info(f"Calling Groq API for personality analysis (prompt length: {len(complete_prompt)} chars)...")
        
        def _groq_analysis():
            return get_groq_response(
                input_text=complete_prompt,
                model="llama-3.3-70b-versatile",  # Use the default model
                history=None,  # No conversation history needed
                system_prompt=None  # Prompt is self-contained
            )
        
        # Use safe API operation with comprehensive error handling
        api_success, analysis_result, api_error_info = safe_api_operation(_groq_analysis)
        
        if not api_success:
            logger.error(f"Groq API operation failed: {api_error_info['message']}")
            return create_error_response(
                error_type='llm_api_failure',
                message=f'LLM API call failed: {api_error_info["message"]}',
                metadata={
                    'conversation_count': conversation_count,
                    'error_category': api_error_info.get('category', 'unknown'),
                    'retry_recommended': api_error_info.get('retry_recommended', True)
                }
            )
        
        logger.info(f"Personality analysis completed successfully: {len(analysis_result)} characters")
        
        # Step 6: Parse and structure the analysis result
        parsed_analysis = parse_personality_analysis(analysis_result)
        
        # Step 7: Create successful response with metadata
        analysis_metadata = aggregated_transcripts.get('metadata', {})
        response = {
            'status': 'success',
            'message': 'Personality analysis completed successfully',
            'analysis': {
                'raw_analysis': analysis_result,
                'parsed_sections': parsed_analysis,
                'analysis_length': len(analysis_result)
            },
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'conversation_count': conversation_count,
                'analysis_successful': True,
                'total_conversations_analyzed': analysis_metadata.get('total_conversations', 0),
                'total_messages_analyzed': analysis_metadata.get('total_messages', 0),
                'total_words_analyzed': analysis_metadata.get('total_words', 0),
                'date_range': analysis_metadata.get('date_range', {}),
                'persona_usage': analysis_metadata.get('persona_usage', {}),
                'prompt_length': len(complete_prompt)
            }
        }
        
        logger.info("Personality analysis response prepared successfully")
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in personality analysis: {e}")
        return {
            'status': 'error',
            'error_type': 'unexpected_error',
            'message': f'Unexpected error during personality analysis: {str(e)}',
            'analysis': None,
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'conversation_count': 0,
                'analysis_successful': False
            }
        }

def parse_personality_analysis(analysis_text: str) -> Dict:
    """
    Parse the LLM personality analysis response into structured sections.
    
    Args:
        analysis_text (str): Raw LLM analysis response
        
    Returns:
        Dict: Parsed analysis sections
    """
    try:
        # Initialize sections dictionary
        sections = {
            'personality_overview': '',
            'emotional_patterns': '',
            'communication_style': '',
            'key_personality_traits': '',
            'behavioral_insights': '',
            'growth_and_development': ''
        }
        
        # Define section headers to look for
        section_headers = {
            'personality_overview': ['## Personality Overview', '## Overview'],
            'emotional_patterns': ['## Emotional Patterns', '## Emotions'],
            'communication_style': ['## Communication Style', '## Communication'],
            'key_personality_traits': ['## Key Personality Traits', '## Personality Traits', '## Traits'],
            'behavioral_insights': ['## Behavioral Insights', '## Behavior'],
            'growth_and_development': ['## Growth and Development', '## Growth']
        }
        
        # Split analysis text into lines for processing
        lines = analysis_text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # Check if this line is a section header
            section_found = False
            for section_key, headers in section_headers.items():
                if any(header in line for header in headers):
                    # Save previous section if exists
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    # Start new section
                    current_section = section_key
                    current_content = []
                    section_found = True
                    break
            
            # If not a header and we have a current section, add to content
            if not section_found and current_section and line:
                current_content.append(line)
        
        # Save the last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # If no sections were found, put everything in overview
        if not any(sections.values()):
            sections['personality_overview'] = analysis_text.strip()
        
        logger.debug(f"Parsed personality analysis into {len([s for s in sections.values() if s])} sections")
        return sections
        
    except Exception as e:
        logger.error(f"Error parsing personality analysis: {e}")
        return {
            'personality_overview': analysis_text.strip(),
            'emotional_patterns': '',
            'communication_style': '',
            'key_personality_traits': '',
            'behavioral_insights': '',
            'growth_and_development': ''
        }

def analyze_brief_conversations() -> Dict:
    """
    Analyze brief conversations when there isn't enough data for full personality analysis.
    Provides a summary of available content even with limited data.
    
    Returns:
        Dict: Brief conversation analysis with available insights
    """
    try:
        logger.info("Starting brief conversation analysis...")
        
        # Check database connection
        if not validate_database_connection():
            logger.error("Database connection validation failed")
            return {
                'status': 'error',
                'error_type': 'database_connection',
                'message': 'Database connection failed. Please ensure the database is accessible.',
                'summary': None,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'conversation_count': 0,
                    'analysis_type': 'brief_conversations'
                }
            }
        
        # Get conversation count and messages
        conversation_count = get_conversation_count()
        all_messages = get_all_user_messages()
        
        if conversation_count == 0 or not all_messages:
            logger.warning("No conversations found for brief analysis")
            return {
                'status': 'no_data',
                'message': 'No conversations found in the database.',
                'summary': None,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'conversation_count': 0,
                    'analysis_type': 'brief_conversations'
                }
            }
        
        # Aggregate available data
        aggregated_data = aggregate_user_transcripts()
        
        # Create brief analysis summary
        brief_summary = create_brief_conversation_summary(aggregated_data, conversation_count)
        
        logger.info(f"Brief conversation analysis completed for {conversation_count} conversations")
        
        return {
            'status': 'success',
            'message': f'Brief analysis completed for {conversation_count} conversation(s)',
            'summary': brief_summary,
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'conversation_count': conversation_count,
                'analysis_type': 'brief_conversations',
                'total_messages': len(all_messages)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in brief conversation analysis: {e}")
        return {
            'status': 'error',
            'error_type': 'unexpected_error',
            'message': f'Error during brief conversation analysis: {str(e)}',
            'summary': None,
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'conversation_count': 0,
                'analysis_type': 'brief_conversations'
            }
        }

def create_brief_conversation_summary(aggregated_data: Dict, conversation_count: int) -> Dict:
    """
    Create a summary of brief conversations with available insights.
    
    Args:
        aggregated_data (Dict): Aggregated conversation data
        conversation_count (int): Number of conversations
        
    Returns:
        Dict: Brief conversation summary with insights
    """
    try:
        if aggregated_data.get('status') != 'success':
            return {
                'overview': 'Unable to analyze conversations due to data processing issues.',
                'conversation_count': conversation_count,
                'insights': [],
                'recommendations': ['Continue having more conversations to enable detailed personality analysis.']
            }
        
        metadata = aggregated_data.get('metadata', {})
        transcripts = aggregated_data.get('transcripts', [])
        
        # Calculate basic statistics
        total_messages = metadata.get('total_messages', 0)
        total_words = metadata.get('total_words', 0)
        avg_messages_per_conversation = metadata.get('average_messages_per_conversation', 0)
        persona_usage = metadata.get('persona_usage', {})
        
        # Generate insights based on available data
        insights = []
        
        # Conversation frequency insights
        if conversation_count > 0:
            if conversation_count == 1:
                insights.append("You've started your journey with one conversation.")
            elif conversation_count < 3:
                insights.append(f"You've had {conversation_count} conversations, showing initial engagement.")
            else:
                insights.append(f"You've engaged in {conversation_count} conversations, demonstrating consistent interaction.")
        
        # Message depth insights
        if avg_messages_per_conversation > 0:
            if avg_messages_per_conversation < 2:
                insights.append("Your conversations tend to be brief exchanges.")
            elif avg_messages_per_conversation < 4:
                insights.append("You engage in moderate-length conversations.")
            else:
                insights.append("You tend to have more detailed conversations.")
        
        # Persona interaction insights
        if persona_usage:
            most_used_persona = max(persona_usage.items(), key=lambda x: x[1]['conversation_count'])
            persona_name = most_used_persona[0].replace('_', ' ').title() if most_used_persona[0] != 'no_persona' else 'General conversations'
            insights.append(f"You most frequently interact with {persona_name}.")
            
            if len(persona_usage) > 1:
                insights.append(f"You've explored {len(persona_usage)} different conversation types.")
        
        # Content analysis insights
        if total_words > 0:
            if total_words < 50:
                insights.append("Your conversations contain brief, focused exchanges.")
            elif total_words < 200:
                insights.append("You express yourself concisely in conversations.")
            else:
                insights.append("You engage in substantive conversations with detailed responses.")
        
        # Analyze conversation topics and patterns
        topic_insights = analyze_conversation_topics(transcripts)
        insights.extend(topic_insights)
        
        # Generate recommendations
        recommendations = generate_brief_conversation_recommendations(conversation_count, avg_messages_per_conversation)
        
        # Create overview
        overview = create_brief_overview(conversation_count, total_messages, insights)
        
        return {
            'overview': overview,
            'conversation_count': conversation_count,
            'total_messages': total_messages,
            'total_words': total_words,
            'average_messages_per_conversation': round(avg_messages_per_conversation, 1),
            'persona_interactions': len(persona_usage),
            'insights': insights,
            'recommendations': recommendations,
            'date_range': metadata.get('date_range', {}),
            'analysis_note': 'This is a preliminary analysis. More detailed personality insights will be available after 5+ conversations.'
        }
        
    except Exception as e:
        logger.error(f"Error creating brief conversation summary: {e}")
        return {
            'overview': 'Unable to generate conversation summary due to processing error.',
            'conversation_count': conversation_count,
            'insights': [],
            'recommendations': ['Please try again later or contact support if the issue persists.']
        }

def analyze_conversation_topics(transcripts: List[Dict]) -> List[str]:
    """
    Analyze conversation topics from brief conversations.
    
    Args:
        transcripts (List[Dict]): List of conversation transcripts
        
    Returns:
        List[str]: List of topic-based insights
    """
    try:
        if not transcripts:
            return []
        
        insights = []
        
        # Analyze conversation titles for themes
        titles = [t.get('title', '') for t in transcripts if t.get('title')]
        
        # Look for common patterns in conversation content
        all_content = ' '.join([t.get('combined_content', '') for t in transcripts])
        
        # Basic keyword analysis for topics
        question_words = ['what', 'how', 'why', 'when', 'where', 'who']
        question_count = sum(1 for word in question_words if word in all_content.lower())
        
        if question_count > 0:
            insights.append("You tend to ask questions, showing curiosity and engagement.")
        
        # Analyze conversation lengths
        message_counts = [t.get('message_count', 0) for t in transcripts]
        if message_counts:
            max_messages = max(message_counts)
            if max_messages > 3:
                insights.append("Some of your conversations develop into deeper exchanges.")
        
        # Look for greeting patterns
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        greeting_count = sum(1 for greeting in greetings if greeting in all_content.lower())
        
        if greeting_count > 0:
            insights.append("You often begin conversations with polite greetings.")
        
        return insights
        
    except Exception as e:
        logger.error(f"Error analyzing conversation topics: {e}")
        return []

def generate_brief_conversation_recommendations(conversation_count: int, avg_messages: float) -> List[str]:
    """
    Generate recommendations for users with brief conversations.
    
    Args:
        conversation_count (int): Number of conversations
        avg_messages (float): Average messages per conversation
        
    Returns:
        List[str]: List of recommendations
    """
    try:
        recommendations = []
        
        # Based on conversation count
        if conversation_count < 5:
            recommendations.append(f"Continue conversing to reach 5+ conversations for detailed personality analysis. You're {conversation_count}/5 of the way there!")
        
        # Based on conversation depth
        if avg_messages < 3:
            recommendations.append("Try having longer conversations to provide more insights for analysis.")
        
        # General recommendations
        recommendations.extend([
            "Explore different conversation topics to showcase various aspects of your personality.",
            "Try interacting with different personas to see how you adapt your communication style.",
            "Share your thoughts and feelings more openly in conversations for richer analysis."
        ])
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return ["Continue having conversations to enable personality analysis."]

def create_brief_overview(conversation_count: int, total_messages: int, insights: List[str]) -> str:
    """
    Create an overview text for brief conversations.
    
    Args:
        conversation_count (int): Number of conversations
        total_messages (int): Total messages sent
        insights (List[str]): List of insights
        
    Returns:
        str: Overview text
    """
    try:
        if conversation_count == 0:
            return "No conversations found. Start chatting to begin building your personality profile!"
        
        elif conversation_count == 1:
            return f"You've started with one conversation containing {total_messages} message(s). This is a great beginning! Continue conversing to build a more comprehensive personality profile."
        
        elif conversation_count < 5:
            primary_insight = insights[0] if insights else "You're building your conversation history."
            return f"{primary_insight} With {conversation_count} conversations and {total_messages} messages, you're making good progress toward the 5 conversations needed for detailed personality analysis."
        
        else:
            return f"Based on your {conversation_count} conversations with {total_messages} messages, here's what we can observe about your communication patterns."
            
    except Exception as e:
        logger.error(f"Error creating brief overview: {e}")
        return "Unable to generate overview summary."

def get_all_user_messages() -> List[Dict]:
    """
    Retrieve all user messages from the database across all conversations.
    Enhanced with comprehensive error handling and retry logic.
    
    Returns:
        List[Dict]: List of user messages with conversation context
    """
    def _get_messages():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query to get all user messages with conversation context
        cursor.execute('''
            SELECT 
                m.id,
                m.conversation_id,
                m.content,
                m.timestamp,
                c.title as conversation_title,
                c.simulation_file as persona_id,
                c.created_at as conversation_created_at
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE m.role = 'user'
            ORDER BY m.timestamp ASC
        ''')
        
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        logger.info(f"Retrieved {len(messages)} user messages from database")
        return messages
    
    # Use safe database operation with error handling
    success, result, error_info = safe_database_operation(_get_messages)
    
    if success:
        return result
    else:
        logger.error(f"Failed to retrieve user messages: {error_info['message']}")
        return []

def get_conversation_count() -> int:
    """
    Get the total number of conversations in the database.
    Enhanced with comprehensive error handling and retry logic.
    
    Returns:
        int: Total number of conversations
    """
    def _get_count():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM conversations')
        count = cursor.fetchone()[0]
        conn.close()
        
        logger.debug(f"Total conversations in database: {count}")
        return count
    
    # Use safe database operation with error handling
    success, result, error_info = safe_database_operation(_get_count)
    
    if success:
        return result
    else:
        logger.error(f"Failed to get conversation count: {error_info['message']}")
        return 0

def check_minimum_conversations(minimum: int = 5) -> Tuple[bool, int]:
    """
    Check if there are enough conversations to generate a user profile.
    
    Args:
        minimum (int): Minimum number of conversations required (default: 5)
        
    Returns:
        Tuple[bool, int]: (has_minimum, actual_count)
    """
    try:
        actual_count = get_conversation_count()
        has_minimum = actual_count >= minimum
        
        logger.info(f"Conversation count check: {actual_count}/{minimum} (minimum met: {has_minimum})")
        return has_minimum, actual_count
        
    except Exception as e:
        logger.error(f"Error checking minimum conversations: {e}")
        return False, 0

def get_user_messages_by_conversation() -> Dict[int, List[Dict]]:
    """
    Retrieve user messages grouped by conversation ID.
    
    Returns:
        Dict[int, List[Dict]]: Dictionary mapping conversation_id to list of user messages
    """
    try:
        all_messages = get_all_user_messages()
        
        # Group messages by conversation_id
        messages_by_conversation = {}
        for message in all_messages:
            conversation_id = message['conversation_id']
            if conversation_id not in messages_by_conversation:
                messages_by_conversation[conversation_id] = []
            messages_by_conversation[conversation_id].append(message)
        
        logger.info(f"Grouped user messages into {len(messages_by_conversation)} conversations")
        return messages_by_conversation
        
    except Exception as e:
        logger.error(f"Error grouping user messages by conversation: {e}")
        return {}

def get_conversation_statistics() -> Dict:
    """
    Get statistics about user conversations for analysis purposes.
    
    Returns:
        Dict: Statistics including total conversations, total messages, date range, etc.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get basic conversation statistics
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT c.id) as total_conversations,
                COUNT(m.id) as total_user_messages,
                MIN(c.created_at) as first_conversation_date,
                MAX(c.updated_at) as last_conversation_date,
                AVG(msg_count.message_count) as avg_messages_per_conversation
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id AND m.role = 'user'
            LEFT JOIN (
                SELECT conversation_id, COUNT(*) as message_count
                FROM messages 
                WHERE role = 'user'
                GROUP BY conversation_id
            ) msg_count ON c.id = msg_count.conversation_id
        ''')
        
        stats = dict(cursor.fetchone())
        
        # Get persona distribution
        cursor.execute('''
            SELECT 
                c.simulation_file as persona_id,
                COUNT(*) as conversation_count,
                COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id AND m.role = 'user'
            WHERE c.simulation_file IS NOT NULL
            GROUP BY c.simulation_file
            ORDER BY conversation_count DESC
        ''')
        
        persona_stats = [dict(row) for row in cursor.fetchall()]
        stats['persona_distribution'] = persona_stats
        
        logger.info(f"Generated conversation statistics: {stats['total_conversations']} conversations, {stats['total_user_messages']} messages")
        return stats
        
    except sqlite3.Error as e:
        logger.error(f"Database error getting conversation statistics: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error getting conversation statistics: {e}")
        return {}
    finally:
        if conn:
            conn.close()

def aggregate_user_transcripts() -> Dict:
    """
    Aggregate user messages from all conversations into a formatted structure for LLM analysis.
    
    Returns:
        Dict: Aggregated transcript data with metadata for personality analysis
    """
    try:
        # Check minimum conversation requirement first
        has_minimum, conversation_count = check_minimum_conversations()
        if not has_minimum:
            logger.warning(f"Insufficient conversations for profile analysis: {conversation_count}/5")
            return {
                'status': 'insufficient_data',
                'message': f'Need at least 5 conversations for profile analysis. Currently have {conversation_count}.',
                'conversation_count': conversation_count,
                'transcripts': []
            }
        
        # Get all user messages and statistics
        all_messages = get_all_user_messages()
        stats = get_conversation_statistics()
        
        if not all_messages:
            logger.warning("No user messages found for transcript aggregation")
            return {
                'status': 'no_data',
                'message': 'No user messages found in database.',
                'conversation_count': conversation_count,
                'transcripts': []
            }
        
        # Group messages by conversation for better context
        messages_by_conversation = {}
        for message in all_messages:
            conv_id = message['conversation_id']
            if conv_id not in messages_by_conversation:
                messages_by_conversation[conv_id] = {
                    'conversation_id': conv_id,
                    'title': message['conversation_title'],
                    'persona_id': message['persona_id'],
                    'created_at': message['conversation_created_at'],
                    'messages': []
                }
            messages_by_conversation[conv_id]['messages'].append({
                'content': message['content'],
                'timestamp': message['timestamp'],
                'message_id': message['id']
            })
        
        # Create aggregated transcript data
        aggregated_transcripts = []
        total_message_count = 0
        
        for conv_id, conv_data in messages_by_conversation.items():
            # Calculate conversation-level statistics
            message_count = len(conv_data['messages'])
            total_message_count += message_count
            
            # Combine all messages from this conversation
            combined_content = ' '.join([msg['content'] for msg in conv_data['messages']])
            
            # Calculate basic metrics
            word_count = len(combined_content.split())
            char_count = len(combined_content)
            
            conversation_summary = {
                'conversation_id': conv_id,
                'title': conv_data['title'],
                'persona_id': conv_data['persona_id'],
                'created_at': conv_data['created_at'],
                'message_count': message_count,
                'word_count': word_count,
                'char_count': char_count,
                'combined_content': combined_content,
                'individual_messages': conv_data['messages']
            }
            
            aggregated_transcripts.append(conversation_summary)
        
        # Sort by conversation creation date for chronological analysis
        aggregated_transcripts.sort(key=lambda x: x['created_at'])
        
        # Create overall summary for LLM analysis
        all_content_combined = ' '.join([t['combined_content'] for t in aggregated_transcripts])
        
        # Generate metadata for analysis context
        persona_usage = {}
        for transcript in aggregated_transcripts:
            persona = transcript['persona_id'] or 'no_persona'
            if persona not in persona_usage:
                persona_usage[persona] = {'conversation_count': 0, 'message_count': 0}
            persona_usage[persona]['conversation_count'] += 1
            persona_usage[persona]['message_count'] += transcript['message_count']
        
        result = {
            'status': 'success',
            'message': f'Successfully aggregated {total_message_count} messages from {len(aggregated_transcripts)} conversations',
            'metadata': {
                'total_conversations': len(aggregated_transcripts),
                'total_messages': total_message_count,
                'total_words': len(all_content_combined.split()),
                'total_characters': len(all_content_combined),
                'date_range': {
                    'first_conversation': aggregated_transcripts[0]['created_at'] if aggregated_transcripts else None,
                    'last_conversation': aggregated_transcripts[-1]['created_at'] if aggregated_transcripts else None
                },
                'persona_usage': persona_usage,
                'average_messages_per_conversation': total_message_count / len(aggregated_transcripts) if aggregated_transcripts else 0
            },
            'transcripts': aggregated_transcripts,
            'combined_content': all_content_combined,
            'conversation_count': len(aggregated_transcripts)
        }
        
        logger.info(f"Successfully aggregated transcripts: {result['metadata']['total_conversations']} conversations, {result['metadata']['total_messages']} messages")
        return result
        
    except Exception as e:
        logger.error(f"Error aggregating user transcripts: {e}")
        return {
            'status': 'error',
            'message': f'Error aggregating transcripts: {str(e)}',
            'conversation_count': 0,
            'transcripts': []
        }

def format_transcripts_for_analysis(aggregated_data: Dict) -> str:
    """
    Format aggregated transcript data into a structured string for LLM analysis.
    
    Args:
        aggregated_data (Dict): Result from aggregate_user_transcripts()
        
    Returns:
        str: Formatted transcript data for LLM analysis
    """
    try:
        if aggregated_data['status'] != 'success':
            return f"Error: {aggregated_data['message']}"
        
        transcripts = aggregated_data['transcripts']
        metadata = aggregated_data['metadata']
        
        # Create formatted analysis input
        formatted_content = []
        
        # Add overall summary
        formatted_content.append("=== USER CONVERSATION ANALYSIS ===")
        formatted_content.append(f"Total Conversations: {metadata['total_conversations']}")
        formatted_content.append(f"Total Messages: {metadata['total_messages']}")
        formatted_content.append(f"Total Words: {metadata['total_words']}")
        formatted_content.append(f"Date Range: {metadata['date_range']['first_conversation']} to {metadata['date_range']['last_conversation']}")
        formatted_content.append("")
        
        # Add persona interaction summary
        formatted_content.append("=== PERSONA INTERACTIONS ===")
        for persona, usage in metadata['persona_usage'].items():
            persona_name = persona if persona != 'no_persona' else 'General Conversation'
            formatted_content.append(f"{persona_name}: {usage['conversation_count']} conversations, {usage['message_count']} messages")
        formatted_content.append("")
        
        # Add individual conversation summaries
        formatted_content.append("=== CONVERSATION TRANSCRIPTS ===")
        for i, transcript in enumerate(transcripts, 1):
            formatted_content.append(f"--- Conversation {i} ---")
            formatted_content.append(f"Title: {transcript['title']}")
            formatted_content.append(f"Persona: {transcript['persona_id'] or 'General'}")
            formatted_content.append(f"Date: {transcript['created_at']}")
            formatted_content.append(f"Messages: {transcript['message_count']}")
            formatted_content.append(f"Content: {transcript['combined_content']}")
            formatted_content.append("")
        
        result = '\n'.join(formatted_content)
        logger.debug(f"Formatted transcript data for analysis: {len(result)} characters")
        return result
        
    except Exception as e:
        logger.error(f"Error formatting transcripts for analysis: {e}")
        return f"Error formatting transcripts: {str(e)}"

def validate_database_connection() -> bool:
    """
    Validate that the database connection is working and required tables exist.
    
    Returns:
        bool: True if database is accessible and valid, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if required tables exist
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('conversations', 'messages')
        ''')
        
        tables = [row[0] for row in cursor.fetchall()]
        required_tables = ['conversations', 'messages']
        
        if not all(table in tables for table in required_tables):
            logger.error(f"Missing required tables. Found: {tables}, Required: {required_tables}")
            return False
        
        logger.debug("Database connection and table validation successful")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Database validation error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during database validation: {e}")
        return False
    finally:
        if conn:
            conn.close()

def validate_groq_api_connection() -> Tuple[bool, str]:
    """
    Validate that the Groq API connection is working and API key is valid.
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        # Import environment variable check
        import os
        
        # Check if API key is set
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.error("GROQ_API_KEY environment variable not set")
            return False, "GROQ_API_KEY environment variable not set"
        
        # Test API connection with minimal request
        logger.info("Testing Groq API connection...")
        test_response = get_groq_response(
            input_text="Hello, this is a test message. Please respond with 'Test successful.'",
            model="llama-3.3-70b-versatile",
            history=None,
            system_prompt="You are a helpful assistant. Respond briefly and clearly."
        )
        
        # Check if response indicates an error
        if test_response.startswith("Error:"):
            logger.error(f"Groq API validation failed: {test_response}")
            return False, f"API validation failed: {test_response}"
        
        # Check if response is reasonable (not empty, not too short)
        if len(test_response.strip()) < 3:
            logger.error(f"Groq API returned invalid response: {test_response}")
            return False, f"API returned invalid response: {test_response}"
        
        logger.info("Groq API connection validation successful")
        return True, "API connection validated successfully"
        
    except Exception as e:
        logger.error(f"Groq API validation error: {e}")
        return False, f"API validation error: {str(e)}"

def retry_with_backoff(func, *args, max_retries: int = 3, base_delay: float = 1.0, **kwargs):
    """
    Retry a function with exponential backoff.
    
    Args:
        func: Function to retry
        *args: Positional arguments for the function
        max_retries (int): Maximum number of retry attempts
        base_delay (float): Base delay in seconds between retries
        **kwargs: Keyword arguments for the function
        
    Returns:
        Function result or raises last exception
    """
    import time
    
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries:
                logger.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                raise e
            
            delay = base_delay * (2 ** attempt)
            logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}), retrying in {delay}s: {e}")
            time.sleep(delay)

def categorize_database_error(error: Exception) -> Dict[str, str]:
    """
    Categorize database errors into specific types for better error handling.
    
    Args:
        error (Exception): The database error to categorize
        
    Returns:
        Dict[str, str]: Error category and user-friendly message
    """
    error_str = str(error).lower()
    
    if "database is locked" in error_str:
        return {
            'category': 'database_locked',
            'message': 'Database is temporarily busy. Please try again in a moment.',
            'retry_recommended': True
        }
    elif "no such table" in error_str:
        return {
            'category': 'missing_table',
            'message': 'Database structure issue. Please reinitialize the database.',
            'retry_recommended': False
        }
    elif "database disk image is malformed" in error_str:
        return {
            'category': 'database_corruption',
            'message': 'Database file is corrupted. Please restore from backup.',
            'retry_recommended': False
        }
    elif "permission denied" in error_str:
        return {
            'category': 'permission_denied',
            'message': 'Database access permission denied. Please check file permissions.',
            'retry_recommended': False
        }
    elif "unable to open database file" in error_str:
        return {
            'category': 'file_access',
            'message': 'Cannot access database file. Please check file path and permissions.',
            'retry_recommended': False
        }
    else:
        return {
            'category': 'unknown_database_error',
            'message': f'Database error occurred: {str(error)}',
            'retry_recommended': True
        }

def categorize_api_error(error_response: str) -> Dict[str, str]:
    """
    Categorize API errors into specific types for better error handling.
    
    Args:
        error_response (str): The API error response
        
    Returns:
        Dict[str, str]: Error category and user-friendly message
    """
    error_str = error_response.lower()
    
    if "api key" in error_str or "authentication" in error_str:
        return {
            'category': 'authentication_error',
            'message': 'API authentication failed. Please check your API key.',
            'retry_recommended': False
        }
    elif "rate limit" in error_str or "too many requests" in error_str:
        return {
            'category': 'rate_limit_error',
            'message': 'API rate limit exceeded. Please try again later.',
            'retry_recommended': True
        }
    elif "network" in error_str or "connection" in error_str or "timeout" in error_str:
        return {
            'category': 'network_error',
            'message': 'Network connection issue. Please check your internet connection.',
            'retry_recommended': True
        }
    elif "service unavailable" in error_str or "internal server error" in error_str:
        return {
            'category': 'service_error',
            'message': 'API service is temporarily unavailable. Please try again later.',
            'retry_recommended': True
        }
    elif "invalid model" in error_str or "model not found" in error_str:
        return {
            'category': 'model_error',
            'message': 'Requested AI model is not available. Please try again.',
            'retry_recommended': False
        }
    elif "content policy" in error_str or "safety" in error_str:
        return {
            'category': 'content_policy_error',
            'message': 'Content policy violation. Please modify your request.',
            'retry_recommended': False
        }
    else:
        return {
            'category': 'unknown_api_error',
            'message': f'API error occurred: {error_response}',
            'retry_recommended': True
        }

def safe_database_operation(operation_func, *args, **kwargs):
    """
    Safely execute a database operation with error handling and retry logic.
    
    Args:
        operation_func: Database operation function to execute
        *args: Positional arguments for the operation
        **kwargs: Keyword arguments for the operation
        
    Returns:
        Tuple[bool, Any, Dict]: (success, result, error_info)
    """
    try:
        # First validate database connection
        if not validate_database_connection():
            return False, None, {
                'category': 'connection_failed',
                'message': 'Database connection validation failed',
                'retry_recommended': True
            }
        
        # Execute operation with retry logic for certain errors
        try:
            result = retry_with_backoff(operation_func, *args, max_retries=2, base_delay=0.5, **kwargs)
            return True, result, None
        except sqlite3.Error as db_error:
            error_info = categorize_database_error(db_error)
            logger.error(f"Database operation failed: {error_info['message']}")
            return False, None, error_info
        except Exception as e:
            logger.error(f"Unexpected error in database operation: {e}")
            return False, None, {
                'category': 'unexpected_error',
                'message': f'Unexpected error: {str(e)}',
                'retry_recommended': True
            }
            
    except Exception as e:
        logger.error(f"Critical error in safe database operation: {e}")
        return False, None, {
            'category': 'critical_error',
            'message': f'Critical error occurred: {str(e)}',
            'retry_recommended': False
        }

def safe_api_operation(api_func, *args, **kwargs):
    """
    Safely execute an API operation with error handling and retry logic.
    
    Args:
        api_func: API operation function to execute
        *args: Positional arguments for the operation
        **kwargs: Keyword arguments for the operation
        
    Returns:
        Tuple[bool, Any, Dict]: (success, result, error_info)
    """
    try:
        # First validate API connection
        api_valid, api_error = validate_groq_api_connection()
        if not api_valid:
            return False, None, {
                'category': 'api_connection_failed',
                'message': api_error,
                'retry_recommended': True
            }
        
        # Execute API operation with retry logic
        try:
            result = retry_with_backoff(api_func, *args, max_retries=2, base_delay=2.0, **kwargs)
            
            # Check if result indicates an error
            if isinstance(result, str) and result.startswith("Error:"):
                error_info = categorize_api_error(result)
                logger.error(f"API operation failed: {error_info['message']}")
                return False, None, error_info
            
            return True, result, None
            
        except Exception as api_error:
            error_info = categorize_api_error(str(api_error))
            logger.error(f"API operation failed: {error_info['message']}")
            return False, None, error_info
            
    except Exception as e:
        logger.error(f"Critical error in safe API operation: {e}")
        return False, None, {
            'category': 'critical_error',
            'message': f'Critical error occurred: {str(e)}',
            'retry_recommended': False
        }

def create_error_response(error_type: str, message: str, metadata: Dict = None) -> Dict:
    """
    Create a standardized error response structure.
    
    Args:
        error_type (str): Type of error (e.g., 'database_error', 'api_error')
        message (str): Error message
        metadata (Dict, optional): Additional metadata
        
    Returns:
        Dict: Standardized error response
    """
    return {
        'status': 'error',
        'error_type': error_type,
        'message': message,
        'analysis': None,
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'conversation_count': metadata.get('conversation_count', 0) if metadata else 0,
            'analysis_successful': False,
            **(metadata or {})
        }
    }

# Test functions for development and debugging
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING USER PROFILE ANALYZER FUNCTIONS")
    print("=" * 60)
    
    # Test 1: Database connection validation
    print("\n1. Testing database connection validation...")
    try:
        is_valid = validate_database_connection()
        print(f"   ✅ Database connection valid: {is_valid}")
    except Exception as e:
        print(f"   ❌ Database connection test failed: {e}")
    
    # Test 2: Conversation count check
    print("\n2. Testing conversation count...")
    try:
        total_conversations = get_conversation_count()
        print(f"   ✅ Total conversations in database: {total_conversations}")
        
        has_minimum, actual_count = check_minimum_conversations()
        print(f"   ✅ Minimum conversations check: {has_minimum} (has {actual_count}/5)")
    except Exception as e:
        print(f"   ❌ Conversation count test failed: {e}")
    
    # Test 3: Retrieving user messages
    print("\n3. Testing user message retrieval...")
    try:
        all_messages = get_all_user_messages()
        print(f"   ✅ Retrieved {len(all_messages)} user messages")
        
        if all_messages:
            sample_message = all_messages[0]
            print(f"   ✅ Sample message keys: {list(sample_message.keys())}")
            print(f"   ✅ Sample content preview: {sample_message.get('content', '')[:100]}...")
        else:
            print("   ⚠️  No user messages found in database")
    except Exception as e:
        print(f"   ❌ User message retrieval test failed: {e}")
    
    # Test 4: Messages grouped by conversation
    print("\n4. Testing message grouping by conversation...")
    try:
        grouped_messages = get_user_messages_by_conversation()
        print(f"   ✅ Messages grouped into {len(grouped_messages)} conversations")
        
        for conv_id, messages in list(grouped_messages.items())[:3]:  # Show first 3
            print(f"   ✅ Conversation {conv_id}: {len(messages)} messages")
    except Exception as e:
        print(f"   ❌ Message grouping test failed: {e}")
    
    # Test 5: Conversation statistics
    print("\n5. Testing conversation statistics...")
    try:
        stats = get_conversation_statistics()
        print(f"   ✅ Statistics generated with keys: {list(stats.keys())}")
        
        if stats:
            print(f"   ✅ Total conversations: {stats.get('total_conversations', 'N/A')}")
            print(f"   ✅ Total user messages: {stats.get('total_user_messages', 'N/A')}")
            print(f"   ✅ Avg messages per conversation: {stats.get('avg_messages_per_conversation', 'N/A')}")
            
            persona_dist = stats.get('persona_distribution', [])
            print(f"   ✅ Persona distribution: {len(persona_dist)} personas")
            for persona in persona_dist[:3]:  # Show first 3
                print(f"      - {persona.get('persona_id', 'Unknown')}: {persona.get('conversation_count', 0)} conversations")
    except Exception as e:
        print(f"   ❌ Conversation statistics test failed: {e}")
    
    # Test 6: Transcript aggregation
    print("\n6. Testing transcript aggregation...")
    try:
        aggregated = aggregate_user_transcripts()
        print(f"   ✅ Aggregation status: {aggregated.get('status', 'unknown')}")
        print(f"   ✅ Aggregation message: {aggregated.get('message', 'No message')}")
        
        if aggregated.get('status') == 'success':
            metadata = aggregated.get('metadata', {})
            print(f"   ✅ Total conversations: {metadata.get('total_conversations', 'N/A')}")
            print(f"   ✅ Total messages: {metadata.get('total_messages', 'N/A')}")
            print(f"   ✅ Total words: {metadata.get('total_words', 'N/A')}")
            print(f"   ✅ Date range: {metadata.get('date_range', {}).get('first_conversation', 'N/A')} to {metadata.get('date_range', {}).get('last_conversation', 'N/A')}")
            
            # Test transcript formatting
            print("\n   6a. Testing transcript formatting...")
            formatted = format_transcripts_for_analysis(aggregated)
            print(f"      ✅ Formatted transcript length: {len(formatted)} characters")
            print(f"      ✅ Formatted preview: {formatted[:200]}...")
        else:
            print(f"   ⚠️  Aggregation not successful: {aggregated.get('message', 'Unknown reason')}")
    except Exception as e:
        print(f"   ❌ Transcript aggregation test failed: {e}")
    
    # Test 7: Prompt template validation
    print("\n7. Testing prompt template validation...")
    try:
        is_valid = validate_prompt_template()
        print(f"   ✅ Prompt template validation: {is_valid}")
        
        template = get_prompt_template()
        print(f"   ✅ Template length: {len(template)} characters")
        print(f"   ✅ Template has placeholder: {'{transcript_data}' in template}")
        
        # Check for required sections
        required_sections = ['ANALYSIS OBJECTIVES', 'OUTPUT FORMAT', 'ANALYSIS GUIDELINES']
        for section in required_sections:
            has_section = section in template
            print(f"   ✅ Has {section}: {has_section}")
    except Exception as e:
        print(f"   ❌ Prompt template validation test failed: {e}")
    
    # Test 8: Complete prompt creation
    print("\n8. Testing complete prompt creation...")
    try:
        # First get aggregated transcripts
        aggregated = aggregate_user_transcripts()
        
        if aggregated.get('status') == 'success':
            complete_prompt = create_personality_analysis_prompt(aggregated)
            print(f"   ✅ Complete prompt created: {len(complete_prompt)} characters")
            print(f"   ✅ Prompt preview: {complete_prompt[:300]}...")
        else:
            print(f"   ⚠️  Cannot create complete prompt: {aggregated.get('message', 'Aggregation failed')}")
    except Exception as e:
        print(f"   ❌ Complete prompt creation test failed: {e}")
    
    # Test 9: LLM personality analysis (NEW - Task 1.4)
    print("\n9. Testing LLM personality analysis...")
    try:
        # Test the complete personality analysis pipeline
        print("   ⚠️  Note: This test may fail if Groq API is not available in current environment")
        analysis_result = analyze_user_personality()
        
        print(f"   ✅ Analysis status: {analysis_result.get('status', 'unknown')}")
        print(f"   ✅ Analysis message: {analysis_result.get('message', 'No message')}")
        
        if analysis_result.get('status') == 'success':
            analysis_data = analysis_result.get('analysis', {})
            metadata = analysis_result.get('metadata', {})
            
            print(f"   ✅ Raw analysis length: {analysis_data.get('analysis_length', 0)} characters")
            print(f"   ✅ Conversations analyzed: {metadata.get('total_conversations_analyzed', 0)}")
            print(f"   ✅ Messages analyzed: {metadata.get('total_messages_analyzed', 0)}")
            print(f"   ✅ Analysis timestamp: {metadata.get('timestamp', 'N/A')}")
            
            # Test parsing
            parsed_sections = analysis_data.get('parsed_sections', {})
            populated_sections = [k for k, v in parsed_sections.items() if v]
            print(f"   ✅ Parsed sections populated: {len(populated_sections)}/{len(parsed_sections)}")
            
            # Show preview of analysis
            raw_analysis = analysis_data.get('raw_analysis', '')
            if raw_analysis:
                print(f"   ✅ Analysis preview: {raw_analysis[:200]}...")
            
        elif analysis_result.get('status') == 'insufficient_data':
            print(f"   ⚠️  Insufficient data: {analysis_result.get('message', 'Unknown reason')}")
        else:
            print(f"   ❌ Analysis failed: {analysis_result.get('message', 'Unknown error')}")
            print(f"   ❌ Error type: {analysis_result.get('error_type', 'unknown')}")
            
    except Exception as e:
        print(f"   ❌ LLM personality analysis test failed: {e}")
        if "groq" in str(e).lower():
            print("   ⚠️  This is expected if Groq API is not available in test environment")
    
    # Test 9a: Test personality analysis parsing function
    print("\n9a. Testing personality analysis parsing...")
    try:
        # Test the parsing function with mock data
        mock_analysis = """## Personality Overview
This user demonstrates a balanced and thoughtful communication style.

## Emotional Patterns
Shows consistent emotional stability with occasional enthusiasm.

## Communication Style
Direct and concise in their interactions.

## Key Personality Traits
- Thoughtful
- Balanced
- Direct
- Curious

## Behavioral Insights
Tends to ask clarifying questions and seeks understanding.

## Growth and Development
Shows increasing confidence over time."""
        
        parsed_result = parse_personality_analysis(mock_analysis)
        print(f"   ✅ Parsed {len([s for s in parsed_result.values() if s])} sections from mock analysis")
        
        # Test each section
        for section_name, content in parsed_result.items():
            has_content = bool(content.strip())
            print(f"   ✅ {section_name}: {'✓' if has_content else '✗'} ({'has content' if has_content else 'empty'})")
            
    except Exception as e:
        print(f"   ❌ Analysis parsing test failed: {e}")
    
    # Test 10: Brief conversation analysis (NEW - Task 1.5)
    print("\n10. Testing brief conversation analysis...")
    try:
        # Test brief conversation analysis
        brief_result = analyze_brief_conversations()
        
        print(f"   ✅ Brief analysis status: {brief_result.get('status', 'unknown')}")
        print(f"   ✅ Brief analysis message: {brief_result.get('message', 'No message')}")
        
        if brief_result.get('status') == 'success':
            summary = brief_result.get('summary', {})
            metadata = brief_result.get('metadata', {})
            
            print(f"   ✅ Analysis type: {metadata.get('analysis_type', 'unknown')}")
            print(f"   ✅ Conversation count: {summary.get('conversation_count', 0)}")
            print(f"   ✅ Total messages: {summary.get('total_messages', 0)}")
            print(f"   ✅ Insights generated: {len(summary.get('insights', []))}")
            print(f"   ✅ Recommendations: {len(summary.get('recommendations', []))}")
            
            # Show sample insights
            insights = summary.get('insights', [])
            if insights:
                print(f"   ✅ Sample insight: {insights[0]}")
                
            # Show overview
            overview = summary.get('overview', '')
            if overview:
                print(f"   ✅ Overview preview: {overview[:100]}...")
        
        elif brief_result.get('status') == 'no_data':
            print(f"   ⚠️  No data available: {brief_result.get('message', 'Unknown reason')}")
        else:
            print(f"   ❌ Brief analysis failed: {brief_result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"   ❌ Brief conversation analysis test failed: {e}")
    
    # Test 11: Error handling functions (NEW - Task 1.6)
    print("\n11. Testing error handling functions...")
    try:
        # Test Groq API connection validation
        print("   11a. Testing Groq API connection validation...")
        try:
            is_api_valid, api_message = validate_groq_api_connection()
            print(f"   ✅ API connection valid: {is_api_valid}")
            print(f"   ✅ API message: {api_message}")
        except Exception as e:
            print(f"   ❌ API connection test failed: {e}")
        
        # Test database error categorization
        print("   11b. Testing database error categorization...")
        try:
            import sqlite3
            test_db_error = sqlite3.Error("database is locked")
            error_info = categorize_database_error(test_db_error)
            print(f"   ✅ Database error categorized: {error_info['category']}")
            print(f"   ✅ Error message: {error_info['message']}")
            print(f"   ✅ Retry recommended: {error_info['retry_recommended']}")
        except Exception as e:
            print(f"   ❌ Database error categorization test failed: {e}")
        
        # Test API error categorization
        print("   11c. Testing API error categorization...")
        try:
            test_api_error = "Error: API key not found"
            error_info = categorize_api_error(test_api_error)
            print(f"   ✅ API error categorized: {error_info['category']}")
            print(f"   ✅ Error message: {error_info['message']}")
            print(f"   ✅ Retry recommended: {error_info['retry_recommended']}")
        except Exception as e:
            print(f"   ❌ API error categorization test failed: {e}")
        
        # Test error response creation
        print("   11d. Testing error response creation...")
        try:
            error_response = create_error_response(
                error_type='test_error',
                message='This is a test error message',
                metadata={'test_key': 'test_value'}
            )
            print(f"   ✅ Error response created: {error_response['status']}")
            print(f"   ✅ Error type: {error_response['error_type']}")
            print(f"   ✅ Error message: {error_response['message']}")
            print(f"   ✅ Has metadata: {'metadata' in error_response}")
        except Exception as e:
            print(f"   ❌ Error response creation test failed: {e}")
        
        # Test safe database operation with a simple function
        print("   11e. Testing safe database operation...")
        try:
            def _test_db_operation():
                return "Database operation successful"
            
            success, result, error_info = safe_database_operation(_test_db_operation)
            print(f"   ✅ Safe database operation success: {success}")
            print(f"   ✅ Result: {result}")
            print(f"   ✅ Error info: {error_info}")
        except Exception as e:
            print(f"   ❌ Safe database operation test failed: {e}")
        
        # Test retry with backoff (using a mock function)
        print("   11f. Testing retry with backoff...")
        try:
            def _mock_function():
                return "Retry function successful"
            
            result = retry_with_backoff(_mock_function, max_retries=1, base_delay=0.1)
            print(f"   ✅ Retry with backoff result: {result}")
        except Exception as e:
            print(f"   ❌ Retry with backoff test failed: {e}")
            
    except Exception as e:
        print(f"   ❌ Error handling functions test failed: {e}")
    
    # Test Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("All functions from tasks 1.1-1.6 have been tested.")
    print("Task 1.6 - Error handling for LLM API failures and database connection issues: COMPLETED")
    print("Check the results above for any failures or warnings.")
    print("If you see '⚠️' warnings, it might indicate insufficient test data.")
    print("If you see '❌' errors, there may be issues that need addressing.")
    print("=" * 60)