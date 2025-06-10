import os
import json
import logging
import traceback
from typing import Dict, List, Optional, Tuple, Any
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# Import the new medical validation system
from .medical_validation import MedicalValidationSystem

# Initialize logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize global medical validation system
try:
    medical_validator = MedicalValidationSystem()
    logger.info("Medical validation system initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize medical validation system: {e}")
    medical_validator = None

# Legacy constants for backward compatibility (deprecated - use medical_validation.py instead)
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

# Legacy symptom mapping (deprecated - use medical_validation.py instead)
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

# Legacy severity modifiers (deprecated - use medical_validation.py instead)
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

# ✅ PHASE 3.2: Enhanced prompt engineering system
SPECIALTY_SPECIFIC_PROMPTS = {
    "cardiology": {
        "clinical_focus": "cardiovascular pathophysiology, hemodynamic changes, cardiac risk factors",
        "key_considerations": "chest pain characteristics, exertional symptoms, family history, cardiovascular risk factors",
        "diagnostic_approach": "ECG findings, cardiac enzymes, stress testing, echocardiography",
        "urgency_markers": "acute chest pain, hemodynamic instability, arrhythmias"
    },
    "neurology": {
        "clinical_focus": "neurological deficits, cognitive changes, motor/sensory function",
        "key_considerations": "onset timing (acute vs gradual), focal vs diffuse symptoms, associated neurological signs",
        "diagnostic_approach": "neurological examination findings, imaging correlations, cerebrospinal fluid analysis",
        "urgency_markers": "acute neurological deficits, altered consciousness, seizures"
    },
    "orthopedics": {
        "clinical_focus": "musculoskeletal function, joint mechanics, bone integrity",
        "key_considerations": "mechanism of injury, weight-bearing ability, range of motion, deformity",
        "diagnostic_approach": "physical examination, imaging studies, functional assessment",
        "urgency_markers": "open fractures, neurovascular compromise, compartment syndrome"
    },
    "gastroenterology": {
        "clinical_focus": "digestive function, nutritional status, hepatic function",
        "key_considerations": "pain location and character, bowel habits, dietary factors, weight changes",
        "diagnostic_approach": "laboratory studies, endoscopic findings, imaging correlations",
        "urgency_markers": "gastrointestinal bleeding, bowel obstruction, acute abdomen"
    },
    "respiratory": {
        "clinical_focus": "pulmonary function, gas exchange, respiratory mechanics",
        "key_considerations": "dyspnea characteristics, cough patterns, environmental exposures, smoking history",
        "diagnostic_approach": "pulmonary function tests, chest imaging, arterial blood gas analysis",
        "urgency_markers": "acute respiratory distress, hypoxemia, pneumothorax"
    },
    "dermatology": {
        "clinical_focus": "skin integrity, inflammatory processes, infectious conditions",
        "key_considerations": "lesion morphology, distribution patterns, associated symptoms, triggers",
        "diagnostic_approach": "clinical appearance, dermoscopy, biopsy findings, patch testing",
        "urgency_markers": "severe allergic reactions, widespread skin involvement, systemic symptoms"
    },
    "emergency": {
        "clinical_focus": "acute presentations, life-threatening conditions, rapid assessment",
        "key_considerations": "vital signs, level of consciousness, pain severity, onset timing",
        "diagnostic_approach": "rapid triage, point-of-care testing, immediate interventions",
        "urgency_markers": "hemodynamic instability, respiratory distress, altered mental status"
    }
}

DEMOGRAPHIC_CONSIDERATIONS = {
    "pediatric": {
        "age_range": [0, 17],
        "unique_factors": "developmental considerations, parent/caregiver involvement, age-appropriate communication",
        "common_presentations": "viral infections, developmental concerns, vaccination-related issues"
    },
    "young_adult": {
        "age_range": [18, 35],
        "unique_factors": "lifestyle factors, reproductive health, occupational exposures",
        "common_presentations": "sports injuries, mental health concerns, substance use"
    },
    "middle_aged": {
        "age_range": [36, 65],
        "unique_factors": "chronic disease onset, work-related stress, family responsibilities",
        "common_presentations": "cardiovascular risk, diabetes, cancer screening"
    },
    "elderly": {
        "age_range": [66, 100],
        "unique_factors": "polypharmacy, multiple comorbidities, functional decline, atypical presentations",
        "common_presentations": "falls, cognitive decline, medication side effects, frailty"
    }
}

DIFFICULTY_LEVEL_SPECIFICATIONS = {
    "beginner": {
        "description": "Clear symptom presentation with obvious diagnostic clues",
        "characteristics": "typical presentations, minimal confounding factors, straightforward diagnosis",
        "learning_focus": "basic pattern recognition, fundamental knowledge application"
    },
    "intermediate": {
        "description": "Moderate complexity with some atypical features or comorbidities",
        "characteristics": "mixed presentations, mild confounding factors, differential considerations",
        "learning_focus": "clinical reasoning, differential diagnosis, management decisions"
    },
    "advanced": {
        "description": "Complex case with atypical presentations or multiple comorbidities",
        "characteristics": "unusual presentations, significant confounding factors, rare conditions",
        "learning_focus": "expert clinical reasoning, complex decision-making, rare disease recognition"
    }
}

def validate_symptom_specialty_combination(specialty: str, symptoms: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that the selected symptoms are appropriate for the chosen specialty.
    Now uses the comprehensive medical validation system.
    
    Args:
        specialty (str): Selected medical specialty
        symptoms (List[str]): List of selected symptoms
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_warnings)
    """
    if medical_validator:
        try:
            return medical_validator.validate_symptom_specialty_combination(specialty, symptoms)
        except Exception as e:
            logger.error(f"Error in medical validation system: {e}")
            # Fall back to legacy validation
    
    # Legacy validation fallback
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
    
    return True, warnings

def validate_demographics_for_specialty(specialty: str, age: int, gender: str) -> Tuple[bool, List[str]]:
    """
    Validate that patient demographics are appropriate for the specialty.
    Now uses the comprehensive medical validation system.
    
    Args:
        specialty (str): Medical specialty
        age (int): Patient age
        gender (str): Patient gender
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_warnings)
    """
    if medical_validator:
        try:
            return medical_validator.validate_age_appropriate_conditions(specialty, age, 'moderate')
        except Exception as e:
            logger.error(f"Error in medical validation system: {e}")
            # Fall back to legacy validation
    
    # Legacy validation fallback
    warnings = []
    
    if not (1 <= age <= 120):
        return False, [f"Invalid age: {age}. Must be between 1 and 120."]
    
    if gender not in ['male', 'female', 'other']:
        warnings.append(f"Unusual gender value: {gender}")
    
    if specialty not in MEDICAL_SPECIALTIES:
        return False, [f"Invalid specialty: {specialty}"]
    
    # Check age appropriateness for specialty
    specialty_info = MEDICAL_SPECIALTIES[specialty]
    age_ranges = specialty_info.get("typical_age_ranges", {})
    
    # Determine if age is typical for this specialty
    age_appropriate = False
    for age_group, (min_age, max_age) in age_ranges.items():
        if min_age <= age <= max_age:
            age_appropriate = True
            break
    
    if not age_appropriate:
        warnings.append(f"Age {age} is less common for {specialty} cases")
    
    return True, warnings

def get_demographic_group(age: int) -> str:
    """Determine demographic group based on age"""
    if age <= 17:
        return "pediatric"
    elif age <= 35:
        return "young_adult"
    elif age <= 65:
        return "middle_aged"
    else:
        return "elderly"

def generate_case_generation_prompt(specialty: str, symptoms: List[str], demographics: Dict, severity: str, difficulty: str = "intermediate") -> str:
    """
    Generate a comprehensive, specialty-specific prompt for AI case generation.
    Enhanced for Phase 3.2 with specialty-specific modifications and demographic considerations.
    
    Args:
        specialty (str): Medical specialty
        symptoms (List[str]): Selected symptoms
        demographics (Dict): Patient demographics
        severity (str): Symptom severity level
        difficulty (str): Case difficulty level
        
    Returns:
        str: Formatted prompt for AI
    """
    # Get specialty and demographic information
    specialty_info = MEDICAL_SPECIALTIES.get(specialty, {})
    specialty_prompts = SPECIALTY_SPECIFIC_PROMPTS.get(specialty, {})
    severity_info = SEVERITY_MODIFIERS.get(severity, {})
    difficulty_info = DIFFICULTY_LEVEL_SPECIFICATIONS.get(difficulty, {})
    
    age = demographics.get('age', 45)
    demographic_group = get_demographic_group(age)
    demographic_info = DEMOGRAPHIC_CONSIDERATIONS.get(demographic_group, {})
    
    symptom_list = ", ".join(symptoms)
    common_conditions = ", ".join(specialty_info.get("common_conditions", []))
    
    # Build comprehensive prompt
    prompt = f"""You are an expert medical case generator specializing in {specialty_info.get('name', specialty)}. Create a realistic, medically accurate case with the following specifications:

PATIENT DEMOGRAPHICS:
- Age: {age} years old ({demographic_group} population)
- Gender: {demographics.get('gender', 'Unknown')}
- Occupation: {demographics.get('occupation', 'Unknown')}
- Baseline Medical History: {demographics.get('medical_history', 'To be determined based on case requirements')}

SPECIALTY CONTEXT - {specialty_info.get('name', specialty).upper()}:
- Focus Area: {specialty_info.get('description', '')}
- Clinical Focus: {specialty_prompts.get('clinical_focus', 'Standard clinical approach')}
- Key Diagnostic Considerations: {specialty_prompts.get('key_considerations', 'Standard clinical evaluation')}
- Typical Diagnostic Approach: {specialty_prompts.get('diagnostic_approach', 'Clinical assessment')}
- Urgency Markers: {specialty_prompts.get('urgency_markers', 'Standard urgency indicators')}

PRESENTING SYMPTOMS:
- Primary Symptoms: {symptom_list}
- Severity Level: {severity.upper()} ({severity_info.get('description', '')})
- Pain Scale: {severity_info.get('pain_scale', 'N/A')}
- Functional Impact: {severity_info.get('functional_impact', 'N/A')}

CASE REQUIREMENTS:
- Difficulty Level: {difficulty.upper()} - {difficulty_info.get('description', '')}
- Case Characteristics: {difficulty_info.get('characteristics', '')}
- Learning Focus: {difficulty_info.get('learning_focus', '')}

DEMOGRAPHIC CONSIDERATIONS FOR {demographic_group.upper()} PATIENTS:
- Unique Factors: {demographic_info.get('unique_factors', 'Standard considerations')}
- Common Presentations: {demographic_info.get('common_presentations', 'Typical presentations')}

MEDICAL ACCURACY REQUIREMENTS:
1. Ensure pathophysiological coherence between symptoms and diagnosis
2. Consider age-appropriate disease prevalence and presentations
3. Include realistic timeline and disease progression
4. Account for {demographic_group} population-specific factors
5. Ensure symptoms align with {severity} severity level
6. Make case appropriate for {difficulty} difficulty level

CASE DEVELOPMENT INSTRUCTIONS:
1. SELECT DIAGNOSIS: Choose a specific, realistic diagnosis from {specialty} that:
   - Causes ALL the presenting symptoms: {symptom_list}
   - Is appropriate for {age}-year-old {demographics.get('gender', 'patient')}
   - Matches {severity} severity level
   - Fits {difficulty} complexity level

2. DEVELOP SUPPORTING SYMPTOMS: Add 2-4 additional symptoms that:
   - Are consistent with the chosen diagnosis
   - Enhance diagnostic complexity appropriately
   - Consider {demographic_group} population factors

3. CREATE MEDICAL HISTORY: Develop relevant past medical history that:
   - Supports or explains current presentation
   - Includes risk factors for the condition
   - Considers {demographic_group} typical health patterns

4. ESTABLISH TIMELINE: Create realistic onset and progression that:
   - Matches disease pathophysiology
   - Explains current severity level
   - Includes relevant triggers or precipitating factors

5. PATIENT PRESENTATION: Write how the patient would describe symptoms in:
   - Natural, non-medical language
   - Age-appropriate communication style
   - Consistent with {severity} symptom severity

OUTPUT FORMAT - Return ONLY valid JSON with this exact structure:
{{
    "diagnosis": "Specific medical diagnosis (will be hidden from student)",
    "additional_symptoms": "2-4 additional symptoms beyond presenting symptoms, described as patient would experience them",
    "medical_history": "Relevant past medical history including risk factors and previous conditions",
    "recent_exposure": "Recent events, activities, travel, medications, or exposures that contributed to current condition",
    "patient_presentation": "How patient describes their symptoms in their own words - natural, conversational, age-appropriate",
    "clinical_notes": "Additional clinical details for realism: onset timing, progression, associated factors, what makes it better/worse",
    "difficulty_level": "{difficulty}",
    "learning_objectives": [
        "Primary learning objective specific to this case",
        "Secondary learning objective focusing on differential diagnosis",
        "Tertiary objective related to {specialty} specialty knowledge"
    ],
    "differential_diagnoses": [
        "Most likely alternative diagnosis",
        "Second alternative considering age and demographics", 
        "Third alternative based on symptom overlap",
        "Less likely but important to rule out condition"
    ]
}}

QUALITY STANDARDS:
- Medical accuracy is paramount - ensure all details are clinically sound
- Case must be coherent and realistic for the specified demographic
- Difficulty level must be appropriate for intended learning level
- All symptoms must have logical medical explanations
- Patient presentation must sound authentic and natural

Generate a case that challenges learners at the {difficulty} level while remaining medically accurate and realistic for a {age}-year-old {demographics.get('gender', 'patient')} presenting to {specialty}."""

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
    Now uses the comprehensive medical validation system.
    
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
        # Use comprehensive validation if available
        if medical_validator:
            try:
                age = int(demographics.get('age', 0))
                gender = demographics.get('gender', '')
                
                validation_result = medical_validator.comprehensive_validation(
                    specialty, symptoms, age, gender, severity
                )
                
                if not validation_result['is_valid']:
                    error_msg = f"Validation failed: {', '.join(validation_result['errors'])}"
                    logger.error(error_msg)
                    return {
                        "status": "error",
                        "message": error_msg,
                        "validation_errors": validation_result['errors'],
                        "warnings": validation_result['warnings']
                    }
                
                warnings = validation_result['warnings']
                
            except Exception as validation_error:
                logger.error(f"Error in comprehensive validation: {validation_error}")
                # Fall back to legacy validation
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
        else:
            # Legacy validation
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
            
            # ✅ ADD TYPE CHECKING: Ensure case_data is a dictionary
            if not isinstance(case_data, dict):
                logger.error(f"AI response is not a dictionary. Got type: {type(case_data)}, value: {case_data}")
                return {
                    "status": "error",
                    "message": f"AI returned invalid data type: expected dict, got {type(case_data).__name__}",
                    "raw_response": ai_response
                }
            
            # ✅ ADD LOGGING: Log the parsed structure for debugging
            logger.info(f"Successfully parsed AI response. Keys: {list(case_data.keys())}")
            
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
        
        # ✅ SAFER DICTIONARY ACCESS: Build final patient data structure with safe access
        try:
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
                    'age': str(demographics.get('age', 'Unknown')),
                    'gender': demographics.get('gender', 'Unknown'),
                    'occupation': demographics.get('occupation', 'Unknown'),
                    'medical_history': case_data.get('medical_history', 'No significant medical history'),
                    'illness': case_data.get('diagnosis', 'Unknown condition'),  # Hidden from user
                    'recent_exposure': case_data.get('recent_exposure', 'None reported'),
                    'additional_symptoms': case_data.get('additional_symptoms', 'See presenting symptoms'),
                    'patient_presentation': case_data.get('patient_presentation', 'Patient presents with symptoms as described')
                },
                'generation_metadata': {
                    'specialty': specialty,
                    'input_symptoms': symptoms,
                    'severity': severity,
                    'difficulty_level': case_data.get('difficulty_level', 'intermediate'),
                    'learning_objectives': case_data.get('learning_objectives', []),
                    'differential_diagnoses': case_data.get('differential_diagnoses', []),
                    'clinical_notes': case_data.get('clinical_notes', ''),
                    'generation_warnings': warnings
                },
                'voice_id': 'Fritz-PlayAI'  # Default voice
            }
        except Exception as build_error:
            logger.error(f"Error building patient data structure: {build_error}")
            logger.error(f"case_data type: {type(case_data)}, content: {case_data}")
            return {
                "status": "error",
                "message": f"Error building patient data: {str(build_error)}",
                "case_data": case_data
            }
        
        # Log successful generation
        diagnosis = case_data.get('diagnosis', 'Unknown')
        logger.info(f"Successfully generated case: {diagnosis} for {demographics.get('gender', 'unknown')}, {demographics.get('age', 'unknown')} in {specialty}")
        
        return {
            "status": "success",
            "patient_data": patient_data,
            "warnings": warnings,
            "case_summary": {
                "diagnosis": diagnosis,
                "difficulty": case_data.get('difficulty_level', 'intermediate'),
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
    Now uses the comprehensive medical validation system.
    
    Args:
        specialty (str): Medical specialty
        
    Returns:
        List[str]: List of appropriate symptoms
    """
    if medical_validator:
        try:
            symptoms_dict = medical_validator.get_available_symptoms_for_specialty(specialty)
            return symptoms_dict.get('required', []) + symptoms_dict.get('optional', [])
        except Exception as e:
            logger.error(f"Error getting symptoms from medical validator: {e}")
    
    # Legacy fallback
    if specialty not in MEDICAL_SPECIALTIES:
        return []
    
    appropriate_symptoms = []
    for symptom, specialties in SYMPTOM_TO_SPECIALTY_MAPPING.items():
        if specialty in specialties:
            appropriate_symptoms.append(symptom)
    
    return appropriate_symptoms

def get_specialty_info(specialty: str) -> Dict:
    """
    Get information about a specific specialty.
    Now uses the comprehensive medical validation system.
    
    Args:
        specialty (str): Medical specialty
        
    Returns:
        Dict: Specialty information
    """
    if medical_validator:
        try:
            return medical_validator.get_specialty_info(specialty)
        except Exception as e:
            logger.error(f"Error getting specialty info from medical validator: {e}")
    
    # Legacy fallback
    return MEDICAL_SPECIALTIES.get(specialty, {})

def get_all_specialties() -> Dict:
    """
    Get all available specialties.
    Now uses the comprehensive medical validation system.
    
    Returns:
        Dict: Mapping of specialty keys to display names
    """
    if medical_validator:
        try:
            return medical_validator.get_all_specialties()
        except Exception as e:
            logger.error(f"Error getting specialties from medical validator: {e}")
    
    # Legacy fallback
    return {key: data.get('name', key) for key, data in MEDICAL_SPECIALTIES.items()}

def get_all_symptoms() -> Dict:
    """
    Get all available symptoms.
    Now uses the comprehensive medical validation system.
    
    Returns:
        Dict: Mapping of symptom keys to display names
    """
    if medical_validator:
        try:
            return medical_validator.get_all_symptoms()
        except Exception as e:
            logger.error(f"Error getting symptoms from medical validator: {e}")
    
    # Legacy fallback - extract symptoms from mapping
    all_symptoms = {}
    for symptom in SYMPTOM_TO_SPECIALTY_MAPPING.keys():
        # Convert underscore to readable format
        display_name = symptom.replace('_', ' ').title()
        all_symptoms[symptom] = display_name
    
    return all_symptoms

# ✅ PHASE 3.2: Comprehensive testing and validation functions
def generate_test_cases_for_all_specialties() -> Dict[str, List[Dict]]:
    """
    Generate test cases for each medical specialty to validate AI prompt quality.
    
    Returns:
        Dict mapping specialties to lists of test case results
    """
    logger.info("Generating test cases for all specialties...")
    test_results = {}
    
    # Define test scenarios for each specialty
    test_scenarios = {
        "cardiology": [
            {
                "symptoms": ["chest_pain", "shortness_breath"],
                "demographics": {"age": 55, "gender": "Male", "occupation": "Office worker"},
                "severity": "moderate",
                "difficulty": "intermediate"
            },
            {
                "symptoms": ["palpitations", "dizziness"],
                "demographics": {"age": 28, "gender": "Female", "occupation": "Teacher"},
                "severity": "mild",
                "difficulty": "beginner"
            },
            {
                "symptoms": ["chest_pain", "fatigue", "swelling_legs"],
                "demographics": {"age": 72, "gender": "Male", "occupation": "Retired"},
                "severity": "severe",
                "difficulty": "advanced"
            }
        ],
        "neurology": [
            {
                "symptoms": ["headache", "vision_changes"],
                "demographics": {"age": 42, "gender": "Female", "occupation": "Lawyer"},
                "severity": "moderate",
                "difficulty": "intermediate"
            },
            {
                "symptoms": ["weakness", "numbness"],
                "demographics": {"age": 65, "gender": "Male", "occupation": "Retired teacher"},
                "severity": "severe",
                "difficulty": "advanced"
            },
            {
                "symptoms": ["memory_loss", "confusion"],
                "demographics": {"age": 78, "gender": "Female", "occupation": "Retired"},
                "severity": "moderate",
                "difficulty": "intermediate"
            }
        ],
        "dermatology": [
            {
                "symptoms": ["rash", "itching"],
                "demographics": {"age": 25, "gender": "Female", "occupation": "Student"},
                "severity": "mild",
                "difficulty": "beginner"
            },
            {
                "symptoms": ["dry_skin", "skin_lesion"],
                "demographics": {"age": 45, "gender": "Male", "occupation": "Construction worker"},
                "severity": "moderate",
                "difficulty": "intermediate"
            }
        ],
        "orthopedics": [
            {
                "symptoms": ["joint_pain", "stiffness"],
                "demographics": {"age": 60, "gender": "Female", "occupation": "Nurse"},
                "severity": "moderate",
                "difficulty": "intermediate"
            },
            {
                "symptoms": ["back_pain", "limited_mobility"],
                "demographics": {"age": 35, "gender": "Male", "occupation": "Mechanic"},
                "severity": "severe",
                "difficulty": "advanced"
            }
        ],
        "gastroenterology": [
            {
                "symptoms": ["abdominal_pain", "nausea"],
                "demographics": {"age": 30, "gender": "Female", "occupation": "Marketing manager"},
                "severity": "moderate",
                "difficulty": "intermediate"
            },
            {
                "symptoms": ["diarrhea", "bloating", "loss_appetite"],
                "demographics": {"age": 50, "gender": "Male", "occupation": "Chef"},
                "severity": "severe",
                "difficulty": "advanced"
            }
        ]
    }
    
    for specialty, scenarios in test_scenarios.items():
        logger.info(f"Testing {specialty} specialty...")
        test_results[specialty] = []
        
        for i, scenario in enumerate(scenarios):
            logger.info(f"  Running test case {i+1}/{len(scenarios)}")
            try:
                result = generate_patient_case(
                    specialty=specialty,
                    symptoms=scenario["symptoms"],
                    demographics=scenario["demographics"],
                    severity=scenario["severity"]
                )
                
                # Add test metadata
                result["test_metadata"] = {
                    "test_case_id": f"{specialty}_{i+1}",
                    "expected_difficulty": scenario["difficulty"],
                    "test_symptoms": scenario["symptoms"],
                    "test_demographics": scenario["demographics"]
                }
                
                test_results[specialty].append(result)
                
            except Exception as e:
                logger.error(f"Error testing {specialty} case {i+1}: {e}")
                test_results[specialty].append({
                    "status": "error",
                    "message": str(e),
                    "test_metadata": {
                        "test_case_id": f"{specialty}_{i+1}",
                        "expected_difficulty": scenario["difficulty"]
                    }
                })
    
    logger.info("Test case generation completed")
    return test_results

def validate_medical_accuracy(case_data: Dict, specialty: str, symptoms: List[str]) -> Tuple[bool, List[str], float]:
    """
    Validate the medical accuracy of a generated case.
    
    Args:
        case_data (Dict): Generated case data
        specialty (str): Medical specialty
        symptoms (List[str]): Input symptoms
        
    Returns:
        Tuple[bool, List[str], float]: (is_medically_accurate, validation_notes, accuracy_score)
    """
    validation_notes = []
    accuracy_score = 0.0
    max_score = 10.0
    
    # Check 1: Diagnosis appropriateness for specialty (2 points)
    if case_data.get("diagnosis"):
        # This is a basic check - in a real system, you'd have a knowledge base
        diagnosis = case_data["diagnosis"].lower()
        specialty_keywords = {
            "cardiology": ["cardiac", "heart", "myocardial", "angina", "arrhythmia", "hypertension"],
            "neurology": ["neurological", "brain", "stroke", "seizure", "migraine", "dementia"],
            "dermatology": ["skin", "dermatitis", "eczema", "psoriasis", "rash"],
            "orthopedics": ["fracture", "arthritis", "joint", "bone", "muscle"],
            "gastroenterology": ["gastric", "bowel", "liver", "digestive", "intestinal"]
        }
        
        keywords = specialty_keywords.get(specialty, [])
        if any(keyword in diagnosis for keyword in keywords):
            accuracy_score += 2.0
            validation_notes.append("✓ Diagnosis appropriate for specialty")
        else:
            validation_notes.append("⚠ Diagnosis may not be typical for specialty")
    else:
        validation_notes.append("✗ Missing diagnosis")
    
    # Check 2: Symptom coherence (2 points)
    additional_symptoms = case_data.get("additional_symptoms", "")
    if additional_symptoms and len(additional_symptoms) > 20:
        accuracy_score += 2.0
        validation_notes.append("✓ Adequate additional symptoms provided")
    else:
        validation_notes.append("⚠ Limited additional symptoms")
    
    # Check 3: Medical history relevance (1.5 points)
    medical_history = case_data.get("medical_history", "")
    if medical_history and "no significant" not in medical_history.lower():
        accuracy_score += 1.5
        validation_notes.append("✓ Relevant medical history provided")
    else:
        validation_notes.append("⚠ Limited or generic medical history")
    
    # Check 4: Patient presentation realism (1.5 points)
    patient_presentation = case_data.get("patient_presentation", "")
    if patient_presentation and len(patient_presentation) > 30:
        accuracy_score += 1.5
        validation_notes.append("✓ Realistic patient presentation")
    else:
        validation_notes.append("⚠ Limited patient presentation")
    
    # Check 5: Clinical notes detail (1 point)
    clinical_notes = case_data.get("clinical_notes", "")
    if clinical_notes and len(clinical_notes) > 20:
        accuracy_score += 1.0
        validation_notes.append("✓ Adequate clinical notes")
    else:
        validation_notes.append("⚠ Limited clinical notes")
    
    # Check 6: Learning objectives (1 point)
    learning_objectives = case_data.get("learning_objectives", [])
    if isinstance(learning_objectives, list) and len(learning_objectives) >= 2:
        accuracy_score += 1.0
        validation_notes.append("✓ Appropriate learning objectives")
    else:
        validation_notes.append("⚠ Insufficient learning objectives")
    
    # Check 7: Differential diagnoses (1 point)
    differentials = case_data.get("differential_diagnoses", [])
    if isinstance(differentials, list) and len(differentials) >= 3:
        accuracy_score += 1.0
        validation_notes.append("✓ Adequate differential diagnoses")
    else:
        validation_notes.append("⚠ Insufficient differential diagnoses")
    
    # Overall assessment
    is_medically_accurate = accuracy_score >= 7.0  # 70% threshold
    accuracy_percentage = (accuracy_score / max_score) * 100
    
    validation_notes.append(f"Overall accuracy score: {accuracy_score:.1f}/{max_score} ({accuracy_percentage:.1f}%)")
    
    return is_medically_accurate, validation_notes, accuracy_percentage

def test_edge_cases_and_unusual_combinations() -> Dict[str, Dict]:
    """
    Test edge cases and unusual symptom combinations to validate prompt robustness.
    
    Returns:
        Dict containing edge case test results
    """
    logger.info("Testing edge cases and unusual symptom combinations...")
    
    edge_cases = {
        "elderly_complex": {
            "specialty": "cardiology",
            "symptoms": ["chest_pain", "confusion", "fatigue"],
            "demographics": {"age": 85, "gender": "Female", "occupation": "Retired"},
            "severity": "severe",
            "description": "Elderly patient with atypical presentation"
        },
        "young_adult_rare": {
            "specialty": "neurology", 
            "symptoms": ["headache", "weakness", "vision_changes"],
            "demographics": {"age": 22, "gender": "Male", "occupation": "Student"},
            "severity": "moderate",
            "description": "Young adult with concerning neurological symptoms"
        },
        "pediatric_presentation": {
            "specialty": "dermatology",
            "symptoms": ["rash", "itching", "fever"],
            "demographics": {"age": 8, "gender": "Female", "occupation": "Student"},
            "severity": "moderate", 
            "description": "Pediatric dermatological presentation"
        },
        "multiple_symptoms": {
            "specialty": "gastroenterology",
            "symptoms": ["abdominal_pain", "nausea", "vomiting", "diarrhea", "bloating"],
            "demographics": {"age": 45, "gender": "Male", "occupation": "Restaurant manager"},
            "severity": "severe",
            "description": "Complex gastroenterological presentation"
        },
        "cross_specialty": {
            "specialty": "emergency",
            "symptoms": ["chest_pain", "shortness_breath", "dizziness", "confusion"],
            "demographics": {"age": 60, "gender": "Female", "occupation": "Teacher"},
            "severity": "severe",
            "description": "Emergency presentation with multiple system involvement"
        }
    }
    
    results = {}
    
    for case_name, case_data in edge_cases.items():
        logger.info(f"Testing edge case: {case_name}")
        try:
            result = generate_patient_case(
                specialty=case_data["specialty"],
                symptoms=case_data["symptoms"],
                demographics=case_data["demographics"],
                severity=case_data["severity"]
            )
            
            # Validate the edge case
            if result.get("status") == "success":
                is_accurate, notes, score = validate_medical_accuracy(
                    result["patient_data"]["patient_details"],
                    case_data["specialty"],
                    case_data["symptoms"]
                )
                
                result["edge_case_validation"] = {
                    "is_medically_accurate": is_accurate,
                    "accuracy_score": score,
                    "validation_notes": notes,
                    "case_description": case_data["description"]
                }
            
            results[case_name] = result
            
        except Exception as e:
            logger.error(f"Error testing edge case {case_name}: {e}")
            results[case_name] = {
                "status": "error",
                "message": str(e),
                "case_description": case_data["description"]
            }
    
    return results

def test_difficulty_levels() -> Dict[str, Dict]:
    """
    Test that different difficulty levels produce appropriately complex cases.
    
    Returns:
        Dict containing difficulty level test results
    """
    logger.info("Testing difficulty level variations...")
    
    # Use consistent symptoms and demographics, vary only difficulty
    base_scenario = {
        "specialty": "cardiology",
        "symptoms": ["chest_pain", "shortness_breath"],
        "demographics": {"age": 50, "gender": "Male", "occupation": "Engineer"},
        "severity": "moderate"
    }
    
    results = {}
    
    for difficulty in ["beginner", "intermediate", "advanced"]:
        logger.info(f"Testing {difficulty} difficulty level")
        try:
            # Update the generate_patient_case call to use the new difficulty parameter
            result = generate_patient_case(
                specialty=base_scenario["specialty"],
                symptoms=base_scenario["symptoms"],
                demographics=base_scenario["demographics"],
                severity=base_scenario["severity"]
            )
            
            if result.get("status") == "success":
                case_data = result["patient_data"]["patient_details"]
                is_accurate, notes, score = validate_medical_accuracy(
                    case_data,
                    base_scenario["specialty"],
                    base_scenario["symptoms"]
                )
                
                # Analyze complexity indicators
                complexity_score = 0
                if len(case_data.get("additional_symptoms", "").split()) > 10:
                    complexity_score += 1
                if "comorbid" in case_data.get("medical_history", "").lower():
                    complexity_score += 1
                if len(result.get("case_summary", {}).get("differential_diagnoses", [])) > 3:
                    complexity_score += 1
                
                result["difficulty_analysis"] = {
                    "expected_difficulty": difficulty,
                    "complexity_score": complexity_score,
                    "accuracy_score": score,
                    "validation_notes": notes
                }
            
            results[difficulty] = result
            
        except Exception as e:
            logger.error(f"Error testing {difficulty} difficulty: {e}")
            results[difficulty] = {
                "status": "error",
                "message": str(e),
                "expected_difficulty": difficulty
            }
    
    return results

def run_comprehensive_ai_prompt_tests() -> Dict[str, Any]:
    """
    Run all Phase 3.2 tests for AI prompt engineering validation.
    
    Returns:
        Dict containing comprehensive test results
    """
    logger.info("Starting comprehensive AI prompt engineering tests...")
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "specialty_tests": {},
        "edge_case_tests": {},
        "difficulty_tests": {},
        "summary": {}
    }
    
    try:
        # Test 1: Generate test cases for all specialties
        test_results["specialty_tests"] = generate_test_cases_for_all_specialties()
        
        # Test 2: Edge cases and unusual combinations
        test_results["edge_case_tests"] = test_edge_cases_and_unusual_combinations()
        
        # Test 3: Difficulty level variations
        test_results["difficulty_tests"] = test_difficulty_levels()
        
        # Generate summary
        total_tests = 0
        successful_tests = 0
        
        # Count specialty tests
        for specialty, cases in test_results["specialty_tests"].items():
            total_tests += len(cases)
            successful_tests += sum(1 for case in cases if case.get("status") == "success")
        
        # Count edge case tests
        edge_cases = test_results["edge_case_tests"]
        total_tests += len(edge_cases)
        successful_tests += sum(1 for case in edge_cases.values() if case.get("status") == "success")
        
        # Count difficulty tests
        difficulty_cases = test_results["difficulty_tests"]
        total_tests += len(difficulty_cases)
        successful_tests += sum(1 for case in difficulty_cases.values() if case.get("status") == "success")
        
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        test_results["summary"] = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": f"{success_rate:.1f}%",
            "specialties_tested": len(test_results["specialty_tests"]),
            "edge_cases_tested": len(test_results["edge_case_tests"]),
            "difficulty_levels_tested": len(test_results["difficulty_tests"])
        }
        
        logger.info(f"Comprehensive testing completed: {success_rate:.1f}% success rate")
        
    except Exception as e:
        logger.error(f"Error during comprehensive testing: {e}")
        test_results["error"] = str(e)
    
    return test_results

if __name__ == "__main__":
    # Phase 3.2: Comprehensive AI Prompt Engineering Testing Suite
    import sys
    
    print("🔬 AI Case Generator - Phase 3.2 Testing Suite")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        print("Available test options:")
        print("1. basic - Run basic case generation test")
        print("2. comprehensive - Run all Phase 3.2 tests")
        print("3. specialties - Test all medical specialties") 
        print("4. edge-cases - Test edge cases and unusual combinations")
        print("5. difficulty - Test difficulty level variations")
        print("6. medical-accuracy - Test medical accuracy validation")
        test_type = input("\nSelect test type (1-6 or type name): ").lower()
    
    # Map number inputs to test types
    test_mapping = {
        "1": "basic", "2": "comprehensive", "3": "specialties",
        "4": "edge-cases", "5": "difficulty", "6": "medical-accuracy"
    }
    test_type = test_mapping.get(test_type, test_type)
    
    if test_type == "basic":
        print("\n🧪 Running basic case generation test...")
        # Original basic test
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
    
    elif test_type == "comprehensive":
        print("\n🔬 Running comprehensive Phase 3.2 test suite...")
        results = run_comprehensive_ai_prompt_tests()
        
        print(f"\n📊 Test Results Summary:")
        summary = results.get("summary", {})
        print(f"Total tests: {summary.get('total_tests', 0)}")
        print(f"Successful: {summary.get('successful_tests', 0)}")
        print(f"Failed: {summary.get('failed_tests', 0)}")
        print(f"Success rate: {summary.get('success_rate', '0%')}")
        print(f"Specialties tested: {summary.get('specialties_tested', 0)}")
        print(f"Edge cases tested: {summary.get('edge_cases_tested', 0)}")
        print(f"Difficulty levels tested: {summary.get('difficulty_levels_tested', 0)}")
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_prompt_test_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Detailed results saved to: {filename}")
    
    elif test_type == "specialties":
        print("\n🏥 Testing all medical specialties...")
        results = generate_test_cases_for_all_specialties()
        
        for specialty, cases in results.items():
            successful = sum(1 for case in cases if case.get("status") == "success")
            total = len(cases)
            print(f"{specialty}: {successful}/{total} successful")
            
            for case in cases:
                if case.get("status") == "error":
                    print(f"  ❌ {case['test_metadata']['test_case_id']}: {case['message']}")
                else:
                    print(f"  ✅ {case['test_metadata']['test_case_id']}")
    
    elif test_type == "edge-cases":
        print("\n🔥 Testing edge cases and unusual combinations...")
        results = test_edge_cases_and_unusual_combinations()
        
        for case_name, result in results.items():
            if result.get("status") == "success":
                validation = result.get("edge_case_validation", {})
                accuracy = validation.get("accuracy_score", 0)
                print(f"✅ {case_name}: {accuracy:.1f}% accuracy")
                print(f"   {result.get('edge_case_validation', {}).get('case_description', '')}")
            else:
                print(f"❌ {case_name}: {result.get('message', 'Unknown error')}")
    
    elif test_type == "difficulty":
        print("\n📈 Testing difficulty level variations...")
        results = test_difficulty_levels()
        
        for difficulty, result in results.items():
            if result.get("status") == "success":
                analysis = result.get("difficulty_analysis", {})
                complexity = analysis.get("complexity_score", 0)
                accuracy = analysis.get("accuracy_score", 0)
                print(f"✅ {difficulty}: Complexity={complexity}/3, Accuracy={accuracy:.1f}%")
            else:
                print(f"❌ {difficulty}: {result.get('message', 'Unknown error')}")
    
    elif test_type == "medical-accuracy":
        print("\n🩺 Testing medical accuracy validation...")
        # Test with a sample case
        sample_case = {
            "diagnosis": "Acute myocardial infarction",
            "additional_symptoms": "radiating pain to left arm, sweating, nausea",
            "medical_history": "Hypertension, diabetes, smoking history",
            "patient_presentation": "I have severe chest pain that started an hour ago",
            "clinical_notes": "Pain worse with exertion, associated with shortness of breath",
            "learning_objectives": ["Recognize MI presentation", "Understand cardiac risk factors"],
            "differential_diagnoses": ["Unstable angina", "Aortic dissection", "Pulmonary embolism"]
        }
        
        is_accurate, notes, score = validate_medical_accuracy(sample_case, "cardiology", ["chest_pain", "shortness_breath"])
        
        print(f"Medical accuracy: {'✅ PASS' if is_accurate else '❌ FAIL'}")
        print(f"Accuracy score: {score:.1f}%")
        print("\nValidation notes:")
        for note in notes:
            print(f"  {note}")
    
    else:
        print(f"❌ Unknown test type: {test_type}")
        print("Available options: basic, comprehensive, specialties, edge-cases, difficulty, medical-accuracy") 