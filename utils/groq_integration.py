import os
import sys
import json
import traceback
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_response(input_text, model="llama-3.3-70b-versatile", history=None, system_prompt=None):
    """
    Get a response from Groq LLM with conversation history support.
    
    Args:
        input_text (str): The text to send to the LLM
        model (str): The Groq model to use
        history (list): Optional conversation history
        system_prompt (str): Optional custom system prompt
        
    Returns:
        str: The LLM response
    """
    # Get Groq API key from environment variable

    api_key=os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY environment variable not set. Please set it with your Groq API key."
    
    # Initialize history if not provided
    if history is None:
        history = []
    
    try:
        # Debug: Print incoming history
        print(f"Processing request with {len(history)} previous messages")
        
        # Initialize Groq client - explicitly use only api_key
        try:
            # Explicitly avoid proxy settings by using only the api_key parameter
            client = Groq(api_key=api_key)
            # Test the client with a simple call to ensure it works
            print("Groq client initialized successfully")
        except Exception as client_error:
            print(f"Error initializing Groq client: {client_error}")
            traceback.print_exc()  # Print full traceback for debugging
            return f"Error: Unable to initialize Groq client: {str(client_error)}"
        
        # Create a default system prompt that should always be included
        default_system_prompt = "You are a helpful assistant. Respond concisely to the user's input."
        
        # NEW: Add your default instructions that should always be included
        always_include_instructions = """
        You are roleplaying as a human patient in a medical interview. You must follow these strict rules:

        Only answer what the doctor specifically asks.
         – Do not volunteer any additional information.
         – Do not assume what the doctor might want next.

        Do not provide context unless asked.
         – If the doctor says "What is your name?", respond with just your name.
         – If the doctor says "Tell me your symptoms," only list the symptoms — no history or emotions unless prompted.

        Do not break character. Do not act like an assistant or model. You are the patient.

        If a question is vague, ask for clarification.

        Be concise, natural, and realistic. Think like a real patient — not like a chatbot.


        Here are some examples of how you should respond:
        Doctor: What is your name?
        Patient: Sarah.

        Doctor: What do you do for work?
        Patient: I'm a nurse.

        Doctor: Why are you here today?
        Patient: My stomach's been hurting since last night.

        """
        
        # Combine the always-included instructions with any custom system prompt
        if system_prompt:
            final_system_prompt = f"{always_include_instructions}\n\n{system_prompt}"
        else:
            final_system_prompt = f"{always_include_instructions}\n\n{default_system_prompt}"
        
        # Construct messages list with the combined system prompt
        messages = [{"role": "system", "content": final_system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": input_text})
        
        # API call
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=model,
            )
            
            return chat_completion.choices[0].message.content
        except Exception as api_error:
            print(f"Error during Groq API call: {api_error}")
            traceback.print_exc()  # Print full traceback for debugging
            return f"Error: Failed to get response from Groq API: {str(api_error)}"
        
    except Exception as e:
        print(f"Unexpected error in get_groq_response: {e}")
        traceback.print_exc()
        return f"Error: Failed to get response from Groq: {str(e)}"

def generate_patient_case(specialty, symptoms, patient_demographics, severity="moderate"):
    """
    Generate a realistic medical case using AI based on specialty and symptoms.
    
    Args:
        specialty (str): Medical specialty (e.g., 'cardiology', 'neurology')
        symptoms (list): List of presenting symptoms
        patient_demographics (dict): Age, gender, occupation, medical_history
        severity (str): Symptom severity level
        
    Returns:
        dict: Generated patient case with hidden diagnosis
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {"error": "GROQ_API_KEY environment variable not set"}
    
    try:
        client = Groq(api_key=api_key)
        
        # Create detailed prompt for case generation
        case_generation_prompt = f"""You are an expert medical educator creating realistic patient simulation cases.

TASK: Generate a complete, medically accurate patient case for {specialty} training.

GIVEN INFORMATION:
- Medical Specialty: {specialty}
- Presenting Symptoms: {', '.join(symptoms)}
- Symptom Severity: {severity}
- Patient Age: {patient_demographics.get('age', 'Unknown')}
- Patient Gender: {patient_demographics.get('gender', 'Unknown')}
- Patient Occupation: {patient_demographics.get('occupation', 'Unknown')}
- Existing Medical History: {patient_demographics.get('medical_history', 'No significant history')}

REQUIREMENTS:
1. Choose ONE specific medical diagnosis that realistically explains the given symptoms
2. Add 2-3 additional relevant symptoms the patient should exhibit (beyond those given)
3. Create realistic medical history that supports this diagnosis
4. Describe recent events/exposures that could have triggered or contributed to the condition
5. Make the case appropriately challenging for medical students/residents

MEDICAL ACCURACY: The case must be clinically sound and realistic. Consider:
- Age/gender prevalence of the condition
- Symptom progression and timing
- Risk factors and triggers
- Appropriate severity level

RETURN FORMAT: Respond with ONLY a valid JSON object in this exact format:
{{
    "diagnosis": "Specific medical diagnosis name",
    "additional_symptoms": "2-3 additional relevant symptoms the patient should exhibit, described naturally",
    "medical_history": "Relevant past medical history that supports this case",
    "recent_exposure": "Recent events, activities, or exposures that contributed to this condition",
    "severity_explanation": "Brief explanation of why symptoms are {severity} severity"
}}

Do not include any text outside the JSON object."""

        # Make API call
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a medical education expert. Generate realistic patient cases in valid JSON format only."},
                {"role": "user", "content": case_generation_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7  # Add some creativity while maintaining medical accuracy
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        try:
            case_data = json.loads(response_text)
            
            # Validate required fields
            required_fields = ['diagnosis', 'additional_symptoms', 'medical_history', 'recent_exposure']
            if not all(field in case_data for field in required_fields):
                return {"error": "Invalid case data generated - missing required fields"}
            
            return {
                "success": True,
                "case_data": case_data
            }
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from AI response: {e}")
            print(f"Raw response: {response_text}")
            return {"error": f"Failed to parse AI response as JSON: {str(e)}"}
            
    except Exception as e:
        print(f"Error generating patient case: {e}")
        traceback.print_exc()
        return {"error": f"Failed to generate patient case: {str(e)}"}

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Get a response from Groq LLM")
    parser.add_argument("--text", type=str, help="Input text to send to LLM")
    parser.add_argument("--model", type=str, default="llama3-8b-8192", help="Groq model to use")
    parser.add_argument("--history-file", type=str, help="JSON file containing conversation history")
    parser.add_argument("--system-prompt", type=str, help="Custom system prompt")
    parser.add_argument("--patient-file", type=str, help="Path to patient simulation JSON file")
    
    args = parser.parse_args()
    
    # Load patient simulation file if provided
    if args.patient_file:
        try:
            with open(args.patient_file, 'r') as f:
                patient_data = json.load(f)
                # Use the prompt template from the file
                system_prompt = patient_data.get('prompt_template')
                # Populate template with patient details if available
                if system_prompt and 'patient_details' in patient_data:
                    system_prompt = system_prompt.format(**patient_data['patient_details'])
                # Use the default doctor question if no input was provided initially
                initial_question = None
                if 'doctor_question' in patient_data:
                    initial_question = patient_data['doctor_question']
                print(f"Loaded patient simulation: {args.patient_file}")
        except Exception as e:
            print(f"Error loading patient file: {str(e)}")
            sys.exit(1)
    else:
        system_prompt = args.system_prompt
        initial_question = None
    
    # Load history if provided
    conversation_history = []
    if args.history_file:
        try:
            with open(args.history_file, 'r') as f:
                conversation_history = json.load(f)
        except Exception as e:
            print(f"Error loading history file: {str(e)}")
            sys.exit(1)
    
    print("Starting conversation with virtual patient. Type 'exit' to end the conversation.")
    print("Type 'save' to save the conversation history to a file.")
    
    # Start conversation loop
    while True:
        # Get input text from arguments, stdin, or prompt
        if args.text:
            input_text = args.text
            # If text was provided via command line, only use it once then prompt for more
            args.text = None
        elif initial_question:
            input_text = initial_question
            initial_question = None
        elif not sys.stdin.isatty():
            input_text = sys.stdin.read().strip()
            # If text was from stdin, we can only read it once, so exit after one response
            break_after = True
        else:
            input_text = input("\nDoctor: ")
        
        # Check for special commands
        if input_text.lower() in ["exit", "quit", "bye"]:
            print("Ending conversation.")
            break
        elif input_text.lower() == "save":
            save_file = input("Enter filename to save conversation history: ")
            try:
                with open(save_file, 'w') as f:
                    json.dump(conversation_history, f, indent=2)
                print(f"Conversation saved to {save_file}")
            except Exception as e:
                print(f"Error saving conversation: {e}")
            continue
            
        if not input_text.strip():
            print("Please enter a question.")
            continue
        
        # Get response
        response = get_groq_response(input_text, args.model, conversation_history, system_prompt)
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": input_text})
        conversation_history.append({"role": "assistant", "content": response})
        
        # Print response
        print("\nPatient:", response)
        
        # If input was from stdin, break after one response
        if 'break_after' in locals() and break_after:
            break 