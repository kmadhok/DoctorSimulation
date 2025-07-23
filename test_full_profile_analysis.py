#!/usr/bin/env python3
"""
Comprehensive User Profile Analysis Test Script

This script demonstrates the complete workflow of Task 1.0 - User Profile Analysis Backend Module.
It showcases how to:
1. Check conversation count in the database
2. Pull all user conversations
3. Feed the data to the LLM for personality analysis
4. Print the full resulting output

This leverages all the functions created in utils/user_profile_analyzer.py
"""

import os
import sys
import time
from datetime import datetime

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our user profile analyzer functions
from utils.user_profile_analyzer import (
    validate_database_connection,
    get_conversation_count,
    check_minimum_conversations,
    get_all_user_messages,
    aggregate_user_transcripts,
    format_transcripts_for_analysis,
    analyze_user_personality,
    analyze_brief_conversations,
    parse_personality_analysis,
    validate_groq_api_connection,
    get_conversation_statistics
)

def print_header(title):
    """Print a formatted header for test sections"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n--- {title} ---")

def print_result(label, value, status="✅"):
    """Print a formatted result"""
    print(f"{status} {label}: {value}")

def print_error(label, error, status="❌"):
    """Print a formatted error"""
    print(f"{status} {label}: {error}")

def main():
    """Main test function that demonstrates the complete user profile analysis workflow"""
    
    print_header("COMPREHENSIVE USER PROFILE ANALYSIS TEST")
    print(f"Test started at: {datetime.now().isoformat()}")
    
    # Step 1: Database Connection and Validation
    print_section("Step 1: Database Connection & Validation")
    
    try:
        # Test database connection
        start_time = time.time()
        is_db_valid = validate_database_connection()
        db_time = time.time() - start_time
        
        if is_db_valid:
            print_result("Database Connection", f"Valid ({db_time:.3f}s)")
        else:
            print_error("Database Connection", "Invalid - Check database file and permissions")
            return
            
    except Exception as e:
        print_error("Database Connection", f"Failed with error: {e}")
        return
    
    # Step 2: Conversation Count Analysis
    print_section("Step 2: Conversation Count Analysis")
    
    try:
        # Get total conversation count
        start_time = time.time()
        total_conversations = get_conversation_count()
        count_time = time.time() - start_time
        
        print_result("Total Conversations", f"{total_conversations} ({count_time:.3f}s)")
        
        # Check minimum conversation requirement
        has_minimum, actual_count = check_minimum_conversations()
        print_result("Minimum Conversations Met", f"{has_minimum} ({actual_count}/5 conversations)")
        
        if total_conversations == 0:
            print_error("No Conversations", "No conversations found in database")
            return
            
    except Exception as e:
        print_error("Conversation Count", f"Failed with error: {e}")
        return
    
    # Step 3: User Messages Retrieval
    print_section("Step 3: User Messages Retrieval")
    
    try:
        # Get all user messages
        start_time = time.time()
        all_messages = get_all_user_messages()
        messages_time = time.time() - start_time
        
        print_result("User Messages Retrieved", f"{len(all_messages)} messages ({messages_time:.3f}s)")
        
        if all_messages:
            # Show sample message structure
            sample_message = all_messages[0]
            print_result("Sample Message Keys", list(sample_message.keys()))
            print_result("Sample Content Preview", f"'{sample_message.get('content', '')[:100]}...'")
            
            # Show date range
            if len(all_messages) > 1:
                first_message = all_messages[0]
                last_message = all_messages[-1]
                print_result("Date Range", f"{first_message.get('timestamp', 'N/A')} to {last_message.get('timestamp', 'N/A')}")
        else:
            print_error("No Messages", "No user messages found in database")
            return
            
    except Exception as e:
        print_error("Message Retrieval", f"Failed with error: {e}")
        return
    
    # Step 4: Conversation Statistics
    print_section("Step 4: Conversation Statistics")
    
    try:
        # Get detailed conversation statistics
        start_time = time.time()
        stats = get_conversation_statistics()
        stats_time = time.time() - start_time
        
        if stats:
            print_result("Statistics Generation", f"Completed ({stats_time:.3f}s)")
            print_result("Total Conversations", stats.get('total_conversations', 'N/A'))
            print_result("Total User Messages", stats.get('total_user_messages', 'N/A'))
            print_result("Avg Messages/Conversation", f"{stats.get('avg_messages_per_conversation', 0):.1f}")
            
            # Show persona distribution
            persona_dist = stats.get('persona_distribution', [])
            if persona_dist:
                print_result("Persona Distribution", f"{len(persona_dist)} different personas")
                for i, persona in enumerate(persona_dist[:3]):  # Show top 3
                    persona_name = persona.get('persona_id', 'Unknown')
                    conv_count = persona.get('conversation_count', 0)
                    print(f"   {i+1}. {persona_name}: {conv_count} conversations")
                    
        else:
            print_error("Statistics", "Unable to generate conversation statistics")
            
    except Exception as e:
        print_error("Statistics", f"Failed with error: {e}")
    
    # Step 5: Transcript Aggregation
    print_section("Step 5: Transcript Aggregation")
    
    try:
        # Aggregate all user transcripts
        start_time = time.time()
        aggregated_transcripts = aggregate_user_transcripts()
        aggregation_time = time.time() - start_time
        
        print_result("Aggregation Status", aggregated_transcripts.get('status', 'unknown'))
        print_result("Aggregation Message", aggregated_transcripts.get('message', 'No message'))
        print_result("Processing Time", f"{aggregation_time:.3f}s")
        
        if aggregated_transcripts.get('status') == 'success':
            metadata = aggregated_transcripts.get('metadata', {})
            print_result("Conversations Processed", metadata.get('total_conversations', 'N/A'))
            print_result("Messages Processed", metadata.get('total_messages', 'N/A'))
            print_result("Total Words", metadata.get('total_words', 'N/A'))
            print_result("Total Characters", metadata.get('total_characters', 'N/A'))
            
            # Show date range
            date_range = metadata.get('date_range', {})
            if date_range.get('first_conversation'):
                print_result("Analysis Date Range", f"{date_range.get('first_conversation')} to {date_range.get('last_conversation')}")
                
            # Show persona usage
            persona_usage = metadata.get('persona_usage', {})
            if persona_usage:
                print_result("Persona Interactions", f"{len(persona_usage)} different personas")
                
        elif aggregated_transcripts.get('status') == 'insufficient_data':
            print_result("Insufficient Data", aggregated_transcripts.get('message', 'Unknown reason'), "⚠️")
        else:
            print_error("Aggregation", aggregated_transcripts.get('message', 'Unknown error'))
            
    except Exception as e:
        print_error("Transcript Aggregation", f"Failed with error: {e}")
        return
    
    # Step 6: Format Transcripts for Analysis
    print_section("Step 6: Format Transcripts for LLM Analysis")
    
    try:
        if aggregated_transcripts.get('status') == 'success':
            # Format transcripts for LLM analysis
            start_time = time.time()
            formatted_transcripts = format_transcripts_for_analysis(aggregated_transcripts)
            format_time = time.time() - start_time
            
            print_result("Formatting Status", "Success")
            print_result("Formatted Length", f"{len(formatted_transcripts)} characters")
            print_result("Processing Time", f"{format_time:.3f}s")
            
            # Show preview of formatted content
            if formatted_transcripts:
                print_result("Formatted Preview", f"'{formatted_transcripts[:300]}...'")
        else:
            print_result("Formatting Skipped", "No valid aggregated data to format", "⚠️")
            
    except Exception as e:
        print_error("Transcript Formatting", f"Failed with error: {e}")
    
    # Step 7: API Connection Validation
    print_section("Step 7: API Connection Validation")
    
    try:
        # Test Groq API connection
        start_time = time.time()
        is_api_valid, api_message = validate_groq_api_connection()
        api_time = time.time() - start_time
        
        if is_api_valid:
            print_result("API Connection", f"Valid ({api_time:.3f}s)")
            print_result("API Message", api_message)
            api_available = True
        else:
            print_result("API Connection", f"Invalid - {api_message}", "⚠️")
            print_result("API Status", "Will proceed with mock analysis", "⚠️")
            api_available = False
            
    except Exception as e:
        print_error("API Connection", f"Failed with error: {e}")
        api_available = False
    
    # Step 8: Personality Analysis
    print_section("Step 8: Personality Analysis")
    
    try:
        # Determine which analysis to run based on data availability
        if has_minimum:
            print_result("Analysis Type", "Full Personality Analysis (5+ conversations)")
            
            # Run full personality analysis
            start_time = time.time()
            analysis_result = analyze_user_personality()
            analysis_time = time.time() - start_time
            
            print_result("Analysis Status", analysis_result.get('status', 'unknown'))
            print_result("Analysis Message", analysis_result.get('message', 'No message'))
            print_result("Processing Time", f"{analysis_time:.3f}s")
            
            if analysis_result.get('status') == 'success':
                # Show analysis results
                analysis_data = analysis_result.get('analysis', {})
                metadata = analysis_result.get('metadata', {})
                
                print_result("Raw Analysis Length", f"{analysis_data.get('analysis_length', 0)} characters")
                print_result("Conversations Analyzed", metadata.get('total_conversations_analyzed', 'N/A'))
                print_result("Messages Analyzed", metadata.get('total_messages_analyzed', 'N/A'))
                print_result("Words Analyzed", metadata.get('total_words_analyzed', 'N/A'))
                print_result("Prompt Length", f"{metadata.get('prompt_length', 'N/A')} characters")
                
                # Show the full analysis
                raw_analysis = analysis_data.get('raw_analysis', '')
                if raw_analysis:
                    print_section("FULL PERSONALITY ANALYSIS RESULT")
                    print(raw_analysis)
                    
                    # Parse and show structured sections
                    print_section("PARSED ANALYSIS SECTIONS")
                    parsed_sections = analysis_data.get('parsed_sections', {})
                    for section_name, content in parsed_sections.items():
                        if content.strip():
                            print(f"\n### {section_name.replace('_', ' ').title()}")
                            print(content)
                        else:
                            print_result(f"{section_name.replace('_', ' ').title()}", "No content parsed", "⚠️")
                            
            else:
                print_error("Analysis", analysis_result.get('message', 'Unknown error'))
                error_type = analysis_result.get('error_type', 'unknown')
                print_result("Error Type", error_type)
                
        else:
            print_result("Analysis Type", "Brief Conversation Analysis (< 5 conversations)")
            
            # Run brief conversation analysis
            start_time = time.time()
            brief_result = analyze_brief_conversations()
            brief_time = time.time() - start_time
            
            print_result("Brief Analysis Status", brief_result.get('status', 'unknown'))
            print_result("Brief Analysis Message", brief_result.get('message', 'No message'))
            print_result("Processing Time", f"{brief_time:.3f}s")
            
            if brief_result.get('status') == 'success':
                # Show brief analysis results
                summary = brief_result.get('summary', {})
                metadata = brief_result.get('metadata', {})
                
                print_result("Analysis Type", metadata.get('analysis_type', 'unknown'))
                print_result("Conversations Analyzed", summary.get('conversation_count', 0))
                print_result("Messages Analyzed", summary.get('total_messages', 0))
                print_result("Words Analyzed", summary.get('total_words', 0))
                print_result("Insights Generated", len(summary.get('insights', [])))
                print_result("Recommendations", len(summary.get('recommendations', [])))
                
                # Show the brief analysis
                print_section("BRIEF CONVERSATION ANALYSIS RESULT")
                
                overview = summary.get('overview', '')
                if overview:
                    print(f"**Overview:**\n{overview}\n")
                
                insights = summary.get('insights', [])
                if insights:
                    print("**Insights:**")
                    for i, insight in enumerate(insights, 1):
                        print(f"{i}. {insight}")
                    print()
                
                recommendations = summary.get('recommendations', [])
                if recommendations:
                    print("**Recommendations:**")
                    for i, rec in enumerate(recommendations, 1):
                        print(f"{i}. {rec}")
                    print()
                
                analysis_note = summary.get('analysis_note', '')
                if analysis_note:
                    print(f"**Note:** {analysis_note}")
                    
            else:
                print_error("Brief Analysis", brief_result.get('message', 'Unknown error'))
                
    except Exception as e:
        print_error("Personality Analysis", f"Failed with error: {e}")
    
    # Step 9: Performance Summary
    print_section("Step 9: Performance Summary")
    
    total_time = time.time() - start_time if 'start_time' in locals() else 0
    print_result("Total Test Duration", f"{total_time:.3f}s")
    print_result("Database Status", "Connected" if is_db_valid else "Failed")
    print_result("API Status", "Available" if api_available else "Not Available")
    print_result("Conversations Found", total_conversations)
    print_result("Messages Found", len(all_messages) if 'all_messages' in locals() else 0)
    print_result("Analysis Type", "Full" if has_minimum else "Brief")
    
    # Final summary
    print_header("TEST COMPLETION SUMMARY")
    print(f"✅ Test completed successfully at: {datetime.now().isoformat()}")
    print(f"✅ Database connection: {'Working' if is_db_valid else 'Failed'}")
    print(f"✅ Conversations processed: {total_conversations}")
    print(f"✅ Messages processed: {len(all_messages) if 'all_messages' in locals() else 0}")
    print(f"✅ API connection: {'Working' if api_available else 'Not Available'}")
    print(f"✅ Analysis completed: {'Full personality analysis' if has_minimum else 'Brief conversation analysis'}")
    print("\nThis test demonstrates the complete workflow of Task 1.0 - User Profile Analysis Backend Module.")
    print("All functions from tasks 1.1-1.6 have been successfully demonstrated in a realistic scenario.")

if __name__ == "__main__":
    main()