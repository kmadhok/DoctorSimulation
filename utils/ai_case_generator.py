import os
import json
import logging
import traceback
from typing import Dict, List, Optional, Tuple
from groq import Groq
from dotenv import load_dotenv

# Initialize logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Medical Knowledge Base
MEDICAL_SPECIALTIES = {
    "cardiology": {
        "name": "Cardiology",
        "description": "Heart and cardiovascular system disorders",
        "common_conditions": ["Myocardial infarction", "Angina", "Heart failure", "Arrhythmia", "Hypertension", "Valvular disease"],
        "typical_age_ranges": {
            "young": [18, 40],
            "middle": [40, 65], 
            "elderly": [65, 100]
        }
    },
    "neurology": {
        "name": "Neurology", 
        "description": "Brain, spinal cord, and nervous system disorders",
        "common_conditions": ["Stroke", "Migraine", "Seizure disorder", "Multiple sclerosis", "Parkinson's disease", "Dementia"],
        "typical_age_ranges": {
            "young": [18, 50],
            "middle": [35, 70],
            "elderly": [60, 100]
        }
    },
    "orthopedics": {
        "name": "Orthopedics",
        "description": "Bones, joints, and musculoskeletal system",
        "common_conditions": ["Fracture", "Arthritis", "Back pain", "Sports injury", "Osteoporosis", "Joint dislocation"],
        "typical_age_ranges": {
            "young": [16, 45],
            "middle": [30, 70],
            "elderly": [50, 100]
        }
    },
    "gastroenterology": {
        "name": "Gastroenterology",
        "description": "Digestive system and gastrointestinal tract",
        "common_conditions": ["GERD", "Peptic ulcer", "Inflammatory bowel disease", "Appendicitis", "Liver disease", "Gallstones"],
        "typical_age_ranges": {
            "young": [18, 45], 
            "middle": [35, 70],
            "elderly": [60, 100]
        }
    },
    "respiratory": {
        "name": "Respiratory Medicine",
        "description": "Lungs and breathing disorders",
        "common_conditions": ["Asthma", "COPD", "Pneumonia", "Bronchitis", "Pulmonary embolism", "Lung cancer"],
        "typical_age_ranges": {
            "young": [18, 50],
            "middle": [40, 70],
            "elderly": [60, 100]
        }
    },
    "dermatology": {
        "name": "Dermatology",
        "description": "Skin, hair, and nail conditions",
        "common_conditions": ["Eczema", "Psoriasis", "Skin cancer", "Acne", "Rash", "Dermatitis"],
        "typical_age_ranges": {
            "young": [16, 40],
            "middle": [30, 65],
            "elderly": [50, 100]
        }
    },
    "emergency": {
        "name": "Emergency Medicine",
        "description": "Acute and urgent medical conditions",
        "common_conditions": ["Trauma", "Chest pain", "Severe headache", "Abdominal pain", "Difficulty breathing", "Allergic reaction"],
        "typical_age_ranges": {
            "young": [16, 50],
            "middle": [35, 70],
            "elderly": [60, 100]
        }
    }
}

SYMPTOM_TO_SPECIALTY_MAPPING = {
    # Cardiology symptoms
    "chest_pain": ["cardiology", "emergency"],
    "shortness_breath": ["cardiology", "respiratory", "emergency"],
    "palpitations": ["cardiology"],
    "dizziness": ["cardiology", "neurology"],
    "fatigue": ["cardiology", "respiratory", "gastroenterology"],
    "swelling_legs": ["cardiology"],
    "irregular_heartbeat": ["cardiology"],
    
    # Neurology symptoms  
    "headache": ["neurology", "emergency"],
    "seizure": ["neurology", "emergency"],
    "memory_loss": ["neurology"],
    "confusion": ["neurology", "emergency"],
    "weakness": ["neurology", "orthopedics"],
    "numbness": ["neurology", "orthopedics"],
    "speech_difficulty": ["neurology", "emergency"],
    "vision_changes": ["neurology"],
    
    # Orthopedics symptoms
    "joint_pain": ["orthopedics"],
    "back_pain": ["orthopedics"],
    "limited_mobility": ["orthopedics"],
    "muscle_pain": ["orthopedics"],
    "bone_pain": ["orthopedics"],
    "stiffness": ["orthopedics"],
    
    # Gastroenterology symptoms
    "abdominal_pain": ["gastroenterology", "emergency"],
    "nausea": ["gastroenterology", "neurology"],
    "vomiting": ["gastroenterology", "neurology", "emergency"],
    "diarrhea": ["gastroenterology"],
    "constipation": ["gastroenterology"],
    "bloating": ["gastroenterology"],
    "loss_appetite": ["gastroenterology"],
    
    # Respiratory symptoms
    "cough": ["respiratory"],
    "wheezing": ["respiratory"],
    "chest_tightness": ["respiratory", "cardiology"],
    "sputum_production": ["respiratory"],
    "difficulty_breathing": ["respiratory", "cardiology", "emergency"],
    
    # Dermatology symptoms
    "rash": ["dermatology"],
    "itching": ["dermatology"],
    "skin_lesion": ["dermatology"],
    "dry_skin": ["dermatology"],
    "skin_discoloration": ["dermatology"],
    
    # Emergency/General symptoms
    "fever": ["emergency", "respiratory", "gastroenterology"],
    "severe_pain": ["emergency", "orthopedics"],
    "rapid_heart_rate": ["cardiology", "emergency"],
    "low_blood_pressure": ["cardiology", "emergency"],
    "high_blood_pressure": ["cardiology"]
}

SEVERITY_MODIFIERS = {
    "mild": {
        "description": "Symptoms are noticeable but not significantly impacting daily activities",
        "pain_scale": "1-3/10",
        "functional_impact": "minimal"
    },
    "moderate": {
        "description": "Symptoms are affecting daily activities and causing concern", 
        "pain_scale": "4-6/10",
        "functional_impact": "moderate limitation"
    },
    "severe": {
        "description": "Symptoms are severely limiting function and causing significant distress",
        "pain_scale": "7-10/10", 
        "functional_impact": "major limitation or inability to function"
    }
}

def validate_symptom_specialty_combination(specialty: str, symptoms: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that the selected symptoms are appropriate for the chosen specialty.
    
    Args:
        specialty (str): Selected medical specialty
        symptoms (List[str]): List of selected symptoms
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_warnings)
    """
    warnings = []
    
    if specialty not in MEDICAL_SPECIALTIES:
        return False, [f"Invalid specialty: {specialty}"]
    
    if not symptoms:
        return False, ["At least one symptom must be selected"]
    
    # Check if symptoms are appropriate for specialty
    specialty_appropriate_symptoms = []
    for symptom in symptoms:
        if symptom in SYMPTOM_TO_SPECIALTY_MAPPING:
            if specialty in SYMPTOM_TO_SPECIALTY_MAPPING[symptom]:
                specialty_appropriate_symptoms.append(symptom)
            else:
                warnings.append(f"Symptom '{symptom}' is unusual for {specialty}")
        else:
            warnings.append(f"Unknown symptom: {symptom}")
    
    # If no symptoms are appropriate for the specialty, it's invalid
    if not specialty_appropriate_symptoms:
        return False, warnings + ["No symptoms are appropriate for the selected specialty"]
    
    # Check for contradictory symptoms (can be expanded)
    contradictory_pairs = [
        ("diarrhea", "constipation"),
        ("high_blood_pressure", "low_blood_pressure")
    ]
    
    for symptom1, symptom2 in contradictory_pairs:
        if symptom1 in symptoms and symptom2 in symptoms:
            warnings.append(f"Contradictory symptoms: {symptom1} and {symptom2}")
    
    return True, warnings

def validate_demographics_for_specialty(specialty: str, age: int, gender: str) -> Tuple[bool, List[str]]:
    """
    Validate demographics against typical patterns for the specialty.
    
    Args:
        specialty (str): Medical specialty
        age (int): Patient age
        gender (str): Patient gender
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_warnings)
    """
    warnings = []
    
    if specialty not in MEDICAL_SPECIALTIES:
        return False, [f"Invalid specialty: {specialty}"]
    
    # Age validation (just warnings, not hard failures)
    specialty_data = MEDICAL_SPECIALTIES[specialty]
    age_ranges = specialty_data.get("typical_age_ranges", {})
    
    is_age_typical = False
    for age_group, (min_age, max_age) in age_ranges.items():
        if min_age <= age <= max_age:
            is_age_typical = True
            break
    
    if not is_age_typical:
        warnings.append(f"Age {age} is atypical for {specialty} cases (consider age-appropriate conditions)")
    
    return True, warnings

def generate_case_generation_prompt(specialty: str, symptoms: List[str], demographics: Dict, severity: str) -> str:
    """
    Generate a comprehensive prompt for AI case generation.
    
    Args:
        specialty (str): Medical specialty
        symptoms (List[str]): Selected symptoms
        demographics (Dict): Patient demographics
        severity (str): Symptom severity level
        
    Returns:
        str: Formatted prompt for AI
    """
    specialty_info = MEDICAL_SPECIALTIES.get(specialty, {})
    severity_info = SEVERITY_MODIFIERS.get(severity, {})
    
    symptom_list = ", ".join(symptoms)
    common_conditions = ", ".join(specialty_info.get("common_conditions", []))
    
    prompt = f"""You are an expert medical case generator. Create a realistic medical case for {specialty_info.get('name', specialty)} with the following parameters:

PATIENT DEMOGRAPHICS:
- Age: {demographics.get('age')} years old
- Gender: {demographics.get('gender')}
- Occupation: {demographics.get('occupation')}
- Medical History: {demographics.get('medical_history', 'To be determined')}

PRESENTING SYMPTOMS:
- Primary symptoms: {symptom_list}
- Severity level: {severity} ({severity_info.get('description', '')})
- Pain scale: {severity_info.get('pain_scale', 'N/A')}
- Functional impact: {severity_info.get('functional_impact', 'N/A')}

SPECIALTY CONTEXT:
- Medical specialty: {specialty_info.get('name')} - {specialty_info.get('description')}
- Common conditions in this specialty: {common_conditions}

INSTRUCTIONS:
1. Generate a specific, realistic medical diagnosis that would cause the presenting symptoms
2. Ensure the diagnosis is appropriate for the patient's age and demographic profile
3. Create additional supporting symptoms that would be consistent with the diagnosis
4. Develop a plausible medical history that supports this case
5. Include recent events or exposures that could have triggered or contributed to the condition
6. Make sure the case is medically coherent and educationally valuable

OUTPUT FORMAT (return valid JSON only):
{{
    "diagnosis": "Specific medical diagnosis (this will be hidden from the student)",
    "additional_symptoms": "Additional symptoms the patient should exhibit beyond the presenting symptoms",
    "medical_history": "Relevant past medical history that supports this diagnosis",
    "recent_exposure": "Recent events, activities, or exposures that contributed to or triggered this condition",
    "patient_presentation": "How the patient would describe their symptoms in their own words",
    "clinical_notes": "Additional clinical details that make this case realistic",
    "difficulty_level": "beginner|intermediate|advanced",
    "learning_objectives": ["Primary learning objective", "Secondary learning objective"],
    "differential_diagnoses": ["Alternative diagnosis 1", "Alternative diagnosis 2", "Alternative diagnosis 3"]
}}

Generate a case that is:
- Medically accurate and realistic
- Appropriate for the specified age and demographics
- Consistent with the severity level
- Educational and challenging but not impossible to diagnose
- Rich in clinical detail without being overly complex

Remember: The diagnosis will be hidden from the student - they will only see the symptoms and demographic information."""

    return prompt

def validate_ai_response(response_data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate the AI-generated case response.
    
    Args:
        response_data (Dict): AI response data
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_errors)
    """
    errors = []
    required_fields = [
        "diagnosis", "additional_symptoms", "medical_history", 
        "recent_exposure", "patient_presentation", "clinical_notes",
        "difficulty_level", "learning_objectives", "differential_diagnoses"
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in response_data:
            errors.append(f"Missing required field: {field}")
        elif not response_data[field]:
            errors.append(f"Empty field: {field}")
    
    # Validate specific field formats
    if "difficulty_level" in response_data:
        valid_levels = ["beginner", "intermediate", "advanced"]
        if response_data["difficulty_level"] not in valid_levels:
            errors.append(f"Invalid difficulty_level. Must be one of: {valid_levels}")
    
    if "learning_objectives" in response_data:
        if not isinstance(response_data["learning_objectives"], list) or len(response_data["learning_objectives"]) < 1:
            errors.append("learning_objectives must be a list with at least one item")
    
    if "differential_diagnoses" in response_data:
        if not isinstance(response_data["differential_diagnoses"], list) or len(response_data["differential_diagnoses"]) < 2:
            errors.append("differential_diagnoses must be a list with at least two items")
    
    # Check for reasonable content lengths
    if "diagnosis" in response_data and len(response_data["diagnosis"]) < 3:
        errors.append("diagnosis is too short")
    
    if "patient_presentation" in response_data and len(response_data["patient_presentation"]) < 20:
        errors.append("patient_presentation is too short - should be a detailed description")
    
    return len(errors) == 0, errors

def generate_patient_case(specialty: str, symptoms: List[str], demographics: Dict, severity: str) -> Dict:
    """
    Generate a comprehensive patient case using AI based on specialty, symptoms, and demographics.
    
    Args:
        specialty (str): Medical specialty (e.g., "cardiology", "neurology")
        symptoms (List[str]): List of presenting symptoms
        demographics (Dict): Patient demographics (age, gender, occupation, medical_history)
        severity (str): Symptom severity ("mild", "moderate", "severe")
        
    Returns:
        Dict: Generated patient case data or error information
    """
    logger.info(f"Generating patient case for specialty: {specialty}, symptoms: {symptoms}, severity: {severity}")
    
    try:
        # Input validation
        validation_result, warnings = validate_symptom_specialty_combination(specialty, symptoms)
        if not validation_result:
            error_msg = f"Invalid input combination: {', '.join(warnings)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "warnings": warnings
            }
        
        # Demographics validation
        age = int(demographics.get('age', 0))
        gender = demographics.get('gender', '')
        demo_valid, demo_warnings = validate_demographics_for_specialty(specialty, age, gender)
        warnings.extend(demo_warnings)
        
        if warnings:
            logger.warning(f"Case generation warnings: {warnings}")
        
        # Generate AI prompt
        ai_prompt = generate_case_generation_prompt(specialty, symptoms, demographics, severity)
        logger.debug(f"Generated AI prompt: {ai_prompt[:200]}...")
        
        # Get Groq API key
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            error_msg = "GROQ_API_KEY environment variable not set"
            logger.error(error_msg)
            return {
                "status": "error", 
                "message": error_msg
            }
        
        # Initialize Groq client
        try:
            client = Groq(api_key=api_key)
        except Exception as client_error:
            logger.error(f"Error initializing Groq client: {client_error}")
            return {
                "status": "error",
                "message": f"Failed to initialize AI client: {str(client_error)}"
            }
        
        # Make AI API call
        try:
            logger.info("Calling Groq API for case generation...")
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert medical case generator. Always respond with valid JSON in the exact format requested."
                    },
                    {
                        "role": "user", 
                        "content": ai_prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,  # Some creativity but still focused
                max_tokens=2000
            )
            
            ai_response = chat_completion.choices[0].message.content
            logger.debug(f"AI response received: {ai_response[:200]}...")
            
        except Exception as api_error:
            logger.error(f"Error during Groq API call: {api_error}")
            return {
                "status": "error",
                "message": f"Failed to generate case with AI: {str(api_error)}"
            }
        
        # Parse AI response
        try:
            # Extract JSON from response (in case there's extra text)
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON object found in AI response")
            
            json_text = ai_response[json_start:json_end]
            case_data = json.loads(json_text)
            
        except (json.JSONDecodeError, ValueError) as parse_error:
            logger.error(f"Error parsing AI response as JSON: {parse_error}")
            logger.error(f"AI response was: {ai_response}")
            return {
                "status": "error",
                "message": f"Failed to parse AI response: {str(parse_error)}",
                "raw_response": ai_response
            }
        
        # Validate AI response
        is_valid, validation_errors = validate_ai_response(case_data)
        if not is_valid:
            logger.error(f"AI response validation failed: {validation_errors}")
            return {
                "status": "error",
                "message": f"Generated case failed validation: {', '.join(validation_errors)}",
                "case_data": case_data
            }
        
        # Build final patient data structure
        patient_data = {
            'type': 'ai_generated',
            'prompt_template': """You are a virtual patient in a clinical simulation. You have been assigned the following profile (for your reference only – you must never reveal the diagnosis itself, only describe symptoms):

  • Age: {age}  
  • Gender: {gender}  
  • Occupation: {occupation}  
  • Relevant medical history: {medical_history}  
  • Underlying illness (secret – do not mention this word or any synonyms): {illness}  
  • Any recent events or exposures: {recent_exposure}  

Your task:
When the "Doctor" (the next speaker) asks you questions, respond as a real patient would – describe what hurts, how you feel, when symptoms started, how they've changed, etc. Under no circumstances mention or hint at the diagnosis name.  
Keep answers concise, natural, and include details like pain quality, timing, triggers, and any self-care you've tried.

Additional symptoms you should exhibit: {additional_symptoms}
How you should present: {patient_presentation}""",
            'patient_details': {
                'age': str(demographics.get('age')),
                'gender': demographics.get('gender'),
                'occupation': demographics.get('occupation'),
                'medical_history': case_data['medical_history'],
                'illness': case_data['diagnosis'],  # Hidden from user
                'recent_exposure': case_data['recent_exposure'],
                'additional_symptoms': case_data['additional_symptoms'],
                'patient_presentation': case_data['patient_presentation']
            },
            'generation_metadata': {
                'specialty': specialty,
                'input_symptoms': symptoms,
                'severity': severity,
                'difficulty_level': case_data.get('difficulty_level'),
                'learning_objectives': case_data.get('learning_objectives', []),
                'differential_diagnoses': case_data.get('differential_diagnoses', []),
                'clinical_notes': case_data.get('clinical_notes'),
                'generation_warnings': warnings
            },
            'voice_id': 'Fritz-PlayAI'  # Default voice
        }
        
        # Log successful generation
        logger.info(f"Successfully generated case: {case_data['diagnosis']} for {demographics.get('gender', 'unknown')}, {demographics.get('age', 'unknown')} in {specialty}")
        
        return {
            "status": "success",
            "patient_data": patient_data,
            "warnings": warnings,
            "case_summary": {
                "diagnosis": case_data['diagnosis'],
                "difficulty": case_data.get('difficulty_level'),
                "learning_objectives": case_data.get('learning_objectives', [])
            }
        }
        
    except Exception as e:
        error_msg = f"Unexpected error in generate_patient_case: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "message": error_msg
        }

def get_available_symptoms_for_specialty(specialty: str) -> List[str]:
    """
    Get list of symptoms appropriate for a given specialty.
    
    Args:
        specialty (str): Medical specialty
        
    Returns:
        List[str]: List of appropriate symptoms
    """
    if specialty not in MEDICAL_SPECIALTIES:
        return []
    
    appropriate_symptoms = []
    for symptom, specialties in SYMPTOM_TO_SPECIALTY_MAPPING.items():
        if specialty in specialties:
            appropriate_symptoms.append(symptom)
    
    return sorted(appropriate_symptoms)

def get_specialty_info(specialty: str) -> Dict:
    """
    Get detailed information about a medical specialty.
    
    Args:
        specialty (str): Medical specialty key
        
    Returns:
        Dict: Specialty information
    """
    return MEDICAL_SPECIALTIES.get(specialty, {})

def get_all_specialties() -> Dict:
    """
    Get all available medical specialties.
    
    Returns:
        Dict: All specialty information
    """
    return MEDICAL_SPECIALTIES

def get_all_symptoms() -> Dict:
    """
    Get all available symptoms with their specialty mappings.
    
    Returns:
        Dict: Symptom to specialty mappings
    """
    return SYMPTOM_TO_SPECIALTY_MAPPING

if __name__ == "__main__":
    # Test the case generator
    test_demographics = {
        "age": 45,
        "gender": "Female", 
        "occupation": "Office manager",
        "medical_history": "Hypertension controlled with medication"
    }
    
    test_symptoms = ["chest_pain", "shortness_breath"]
    test_specialty = "cardiology"
    test_severity = "moderate"
    
    print("Testing AI case generator...")
    result = generate_patient_case(test_specialty, test_symptoms, test_demographics, test_severity)
    
    if result["status"] == "success":
        print("✅ Case generation successful!")
        print(f"Generated diagnosis: {result['case_summary']['diagnosis']}")
        print(f"Difficulty: {result['case_summary']['difficulty']}")
        print(f"Learning objectives: {result['case_summary']['learning_objectives']}")
    else:
        print("❌ Case generation failed:")
        print(f"Error: {result['message']}") 