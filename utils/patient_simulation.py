import json
import os
from typing import Dict, Optional

def load_patient_simulation(file_path: str) -> Dict:
    """
    Load patient simulation data from a JSON file.
    
    Args:
        file_path (str): Path to the patient simulation JSON file
        
    Returns:
        Dict: Patient simulation data
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading patient simulation file: {str(e)}")
        return {}

def format_patient_prompt(patient_data: Dict) -> str:
    """
    Format the patient prompt template with patient details.
    
    Args:
        patient_data (Dict): Patient simulation data
        
    Returns:
        str: Formatted prompt
    """
    if not patient_data:
        return ""
        
    prompt_template = patient_data.get("prompt_template", "")
    patient_details = patient_data.get("patient_details", {})
    
    # Format the prompt template with patient details
    formatted_prompt = prompt_template.format(
        age=patient_details.get("age", ""),
        gender=patient_details.get("gender", ""),
        occupation=patient_details.get("occupation", ""),
        medical_history=patient_details.get("medical_history", ""),
        illness=patient_details.get("illness", ""),
        recent_exposure=patient_details.get("recent_exposure", ""),
        additional_symptoms=patient_details.get("additional_symptoms", ""),
        patient_presentation=patient_details.get("patient_presentation", "")
    )
    
    return formatted_prompt

def get_patient_system_prompt(patient_data: Dict) -> str:
    """
    Get the system prompt for the patient simulation.
    
    Args:
        patient_data (Dict): Patient simulation data
        
    Returns:
        str: System prompt
    """
    return format_patient_prompt(patient_data) 