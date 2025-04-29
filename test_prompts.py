#!/usr/bin/env python3
import os
import sys
import json
import argparse
from utils.groq_integration import get_groq_response

def load_prompts_from_file(file_path):
    """Load prompts from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading prompts file: {str(e)}")
        sys.exit(1)

def load_markdown_prompt(file_path):
    """Load a prompt from a markdown file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading markdown prompt file: {str(e)}")
        sys.exit(1)

def run_interactive_mode(model="llama3-8b-8192"):
    """Run in interactive mode with conversation history support."""
    history = []
    system_prompt = input("Enter system prompt (or press Enter for default): ").strip()
    system_prompt = system_prompt if system_prompt else None
    
    print("\n--- Starting conversation (type 'exit' to quit) ---\n")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ('exit', 'quit'):
            print("Exiting conversation.")
            break
            
        response = get_groq_response(
            input_text=user_input,
            model=model,
            history=history,
            system_prompt=system_prompt
        )
        
        print(f"\nGroq: {response}")
        
        # Update history
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response})

def run_prompt_comparison(input_text, prompts_dict, model="llama3-8b-8192"):
    """Compare responses with different system prompts."""
    results = {}
    
    print(f"Testing {len(prompts_dict)} different prompts with input: \"{input_text}\"\n")
    
    for prompt_name, prompt_text in prompts_dict.items():
        print(f"Testing prompt: {prompt_name}")
        response = get_groq_response(
            input_text=input_text,
            model=model,
            system_prompt=prompt_text
        )
        results[prompt_name] = response
        print(f"Response: {response}\n")
    
    # Save results to file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prompt_comparison_{timestamp}.json"
    
    output = {
        "input": input_text,
        "model": model,
        "prompts": prompts_dict,
        "responses": results
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to {filename}")

def run_patient_simulation(doctor_question, patient_details, markdown_file, model="llama3-8b-8192"):
    """Run a patient simulation using a prompt template from a markdown file."""
    # Load the prompt template
    prompt_template = load_markdown_prompt(markdown_file)
    
    # Format the prompt with patient details
    formatted_prompt = prompt_template.format(**patient_details)
    
    print(f"\n--- Running Patient Simulation ---")
    print(f"Patient profile: {patient_details}")
    print(f"Doctor's question: {doctor_question}\n")
    
    # Add the doctor's question to the prompt
    input_text = f"Doctor: \"{doctor_question}\"\nPatient:"
    
    # Get response from Groq
    response = get_groq_response(
        input_text=input_text,
        model=model,
        system_prompt=formatted_prompt
    )
    
    print(f"\nPatient response:\n{response}\n")
    
    # Save the simulation to file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"patient_simulation_{timestamp}.json"
    
    output = {
        "prompt_template": prompt_template,
        "patient_details": patient_details,
        "doctor_question": doctor_question,
        "patient_response": response,
        "model": model
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Simulation saved to {filename}")
    
    return response

# Sample patient profiles
PATIENT_PROFILES = {
    "migraine": {
        "age": "45",
        "gender": "Female",
        "occupation": "Office manager",
        "medical_history": "Hypertension, controlled with medication",
        "illness": "Migraine",
        "recent_exposure": "Working long hours with poor lighting"
    },
    "appendicitis": {
        "age": "28",
        "gender": "Male",
        "occupation": "Software developer",
        "medical_history": "None significant",
        "illness": "Appendicitis",
        "recent_exposure": "Recent food poisoning episode 2 weeks ago"
    },
    "covid": {
        "age": "35",
        "gender": "Non-binary",
        "occupation": "Teacher",
        "medical_history": "Asthma, controlled with inhalers",
        "illness": "COVID-19",
        "recent_exposure": "Recently attended a large indoor conference"
    }
}

if __name__ == "__main__":
    import datetime
    
    parser = argparse.ArgumentParser(description="Test different prompts with Groq LLM")
    parser.add_argument("--model", type=str, default="llama3-8b-8192", help="Groq model to use")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive conversation mode")
    parser.add_argument("--prompts-file", type=str, help="JSON file containing multiple prompts to compare")
    parser.add_argument("--input", type=str, help="Input text to test with different prompts")
    parser.add_argument("--patient-simulation", action="store_true", help="Run patient simulation mode")
    parser.add_argument("--prompt-template", type=str, default="prompts/patient_simulation.md", 
                      help="Markdown file containing the patient simulation prompt template")
    parser.add_argument("--doctor-question", type=str, default="What brings you in today?", 
                      help="Doctor's question to the patient")
    parser.add_argument("--patient-profile", type=str, default="migraine",
                      choices=PATIENT_PROFILES.keys(),
                      help="Predefined patient profile to use")
    parser.add_argument("--age", type=str, help="Patient age (overrides profile)")
    parser.add_argument("--gender", type=str, help="Patient gender (overrides profile)")
    parser.add_argument("--occupation", type=str, help="Patient occupation (overrides profile)")
    parser.add_argument("--medical-history", type=str, help="Patient medical history (overrides profile)")
    parser.add_argument("--illness", type=str, help="Patient illness (overrides profile)")
    parser.add_argument("--recent-exposure", type=str, help="Patient recent exposure (overrides profile)")
    
    args = parser.parse_args()
    
    if args.patient_simulation:
        # Get the base patient details from the selected profile
        patient_details = PATIENT_PROFILES[args.patient_profile].copy()
        
        # Override with any provided CLI arguments
        if args.age:
            patient_details["age"] = args.age
        if args.gender:
            patient_details["gender"] = args.gender
        if args.occupation:
            patient_details["occupation"] = args.occupation
        if args.medical_history:
            patient_details["medical_history"] = args.medical_history
        if args.illness:
            patient_details["illness"] = args.illness
        if args.recent_exposure:
            patient_details["recent_exposure"] = args.recent_exposure
        
        run_patient_simulation(
            doctor_question=args.doctor_question,
            patient_details=patient_details,
            markdown_file=args.prompt_template,
            model=args.model
        )
    elif args.interactive:
        run_interactive_mode(args.model)
    elif args.prompts_file and args.input:
        prompts = load_prompts_from_file(args.prompts_file)
        run_prompt_comparison(args.input, prompts, args.model)
    else:
        # If no specific mode is selected, default to interactive
        print("No mode specified. Running in interactive mode.")
        run_interactive_mode(args.model) 