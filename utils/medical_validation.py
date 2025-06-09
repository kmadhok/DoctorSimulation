import json
import os
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

# Initialize logger
logger = logging.getLogger(__name__)

class MedicalValidationSystem:
    """
    Comprehensive medical validation system for AI-powered patient case generation.
    Uses medical_knowledge.json as the source of truth for all validation rules.
    """
    
    def __init__(self, knowledge_file_path: str = None):
        """
        Initialize the medical validation system.
        
        Args:
            knowledge_file_path (str): Path to medical_knowledge.json file
        """
        if knowledge_file_path is None:
            # Default to medical_knowledge.json in the same directory as this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            knowledge_file_path = os.path.join(os.path.dirname(current_dir), 'medical_knowledge.json')
        
        self.knowledge_file_path = knowledge_file_path
        self.medical_knowledge = self._load_medical_knowledge()
        
        # Extract commonly used data for faster access
        self.specialties = self.medical_knowledge.get('medical_specialties', {})
        self.symptoms = self.medical_knowledge.get('symptoms', {})
        self.validation_rules = self.medical_knowledge.get('validation_rules', {})
        self.severity_descriptions = self.medical_knowledge.get('severity_descriptions', {})
        
        logger.info(f"MedicalValidationSystem initialized with {len(self.specialties)} specialties and {len(self.symptoms)} symptoms")
    
    def _load_medical_knowledge(self) -> Dict[str, Any]:
        """
        Load medical knowledge from JSON file.
        
        Returns:
            Dict containing the medical knowledge data
        """
        try:
            with open(self.knowledge_file_path, 'r', encoding='utf-8') as file:
                knowledge = json.load(file)
                logger.info(f"Successfully loaded medical knowledge from {self.knowledge_file_path}")
                return knowledge
        except FileNotFoundError:
            logger.error(f"Medical knowledge file not found: {self.knowledge_file_path}")
            raise FileNotFoundError(f"Medical knowledge file not found: {self.knowledge_file_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in medical knowledge file: {e}")
            raise ValueError(f"Invalid JSON in medical knowledge file: {e}")
        except Exception as e:
            logger.error(f"Error loading medical knowledge: {e}")
            raise
    
    def validate_specialty(self, specialty: str) -> Tuple[bool, List[str]]:
        """
        Validate if a specialty exists and is properly defined.
        
        Args:
            specialty (str): Medical specialty to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        if not specialty:
            errors.append("Specialty cannot be empty")
            return False, errors
        
        if specialty not in self.specialties:
            errors.append(f"Unknown specialty: {specialty}")
            available = ", ".join(self.specialties.keys())
            errors.append(f"Available specialties: {available}")
            return False, errors
        
        # Validate specialty structure
        specialty_data = self.specialties[specialty]
        required_fields = ['name', 'description', 'common_conditions']
        
        for field in required_fields:
            if field not in specialty_data:
                errors.append(f"Specialty {specialty} is missing required field: {field}")
        
        if errors:
            return False, errors
        
        logger.debug(f"Specialty '{specialty}' validated successfully")
        return True, []
    
    def validate_symptoms(self, symptoms: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate a list of symptoms.
        
        Args:
            symptoms (List[str]): List of symptoms to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        if not symptoms:
            errors.append("At least one symptom must be provided")
            return False, errors
        
        # Check each symptom exists
        unknown_symptoms = []
        for symptom in symptoms:
            if symptom not in self.symptoms:
                unknown_symptoms.append(symptom)
        
        if unknown_symptoms:
            errors.append(f"Unknown symptoms: {', '.join(unknown_symptoms)}")
            available = ", ".join(list(self.symptoms.keys())[:10])  # Show first 10
            errors.append(f"Available symptoms (first 10): {available}...")
        
        if errors:
            return False, errors
        
        logger.debug(f"Validated {len(symptoms)} symptoms successfully")
        return True, []
    
    def validate_symptom_specialty_combination(self, specialty: str, symptoms: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate that selected symptoms are appropriate for the chosen specialty.
        
        Args:
            specialty (str): Selected medical specialty
            symptoms (List[str]): List of selected symptoms
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_warnings_and_errors)
        """
        errors = []
        warnings = []
        
        # First validate specialty and symptoms individually
        specialty_valid, specialty_errors = self.validate_specialty(specialty)
        symptoms_valid, symptom_errors = self.validate_symptoms(symptoms)
        
        if not specialty_valid:
            errors.extend(specialty_errors)
        if not symptoms_valid:
            errors.extend(symptom_errors)
        
        if errors:
            return False, errors
        
        # Get validation rules for this specialty
        specialty_rules = self.validation_rules.get('symptom_specialty_combinations', {}).get(specialty, {})
        
        if not specialty_rules:
            warnings.append(f"No specific validation rules found for specialty: {specialty}")
        else:
            # Check symptom appropriateness
            required_symptoms = specialty_rules.get('required_symptoms', [])
            optional_symptoms = specialty_rules.get('optional_symptoms', [])
            contraindicated_symptoms = specialty_rules.get('contraindicated_symptoms', [])
            
            appropriate_symptoms = required_symptoms + optional_symptoms
            
            # Check for contraindicated symptoms
            contraindicated_found = [s for s in symptoms if s in contraindicated_symptoms]
            if contraindicated_found:
                errors.append(f"Contraindicated symptoms for {specialty}: {', '.join(contraindicated_found)}")
            
            # Check if at least one appropriate symptom is present
            appropriate_found = [s for s in symptoms if s in appropriate_symptoms]
            if not appropriate_found:
                warnings.append(f"No typical symptoms found for {specialty}. Consider symptoms from: {', '.join(appropriate_symptoms[:5])}")
            
            # Warn about unusual symptoms
            unusual_symptoms = []
            for symptom in symptoms:
                symptom_data = self.symptoms.get(symptom, {})
                associated_specialties = symptom_data.get('associated_specialties', [])
                if specialty not in associated_specialties:
                    unusual_symptoms.append(symptom)
            
            if unusual_symptoms:
                warnings.append(f"Unusual symptoms for {specialty}: {', '.join(unusual_symptoms)}")
        
        # Check symptom count requirements
        min_max_rules = self.validation_rules.get('minimum_maximum_symptoms', {}).get(specialty, {})
        if min_max_rules:
            min_symptoms = min_max_rules.get('min', 1)
            max_symptoms = min_max_rules.get('max', 10)
            
            if len(symptoms) < min_symptoms:
                errors.append(f"Too few symptoms for {specialty}. Minimum: {min_symptoms}, provided: {len(symptoms)}")
            elif len(symptoms) > max_symptoms:
                errors.append(f"Too many symptoms for {specialty}. Maximum: {max_symptoms}, provided: {len(symptoms)}")
        
        # Combine errors and warnings
        all_messages = errors + warnings
        is_valid = len(errors) == 0
        
        logger.debug(f"Symptom-specialty validation for {specialty}: {is_valid}")
        return is_valid, all_messages
    
    def check_contradictory_symptoms(self, symptoms: List[str]) -> Tuple[bool, List[str]]:
        """
        Check for contradictory symptoms that cannot occur together.
        
        Args:
            symptoms (List[str]): List of symptoms to check
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_contradictions)
        """
        contradictions = []
        contradictory_rules = self.validation_rules.get('contradictory_symptoms', [])
        
        for rule in contradictory_rules:
            conflicting_symptoms = rule.get('symptoms', [])
            reason = rule.get('reason', 'Symptoms are contradictory')
            
            # Check if multiple contradictory symptoms are present
            found_symptoms = [s for s in symptoms if s in conflicting_symptoms]
            if len(found_symptoms) > 1:
                contradictions.append(f"{reason}: {', '.join(found_symptoms)}")
        
        is_valid = len(contradictions) == 0
        logger.debug(f"Contradictory symptoms check: {is_valid}")
        return is_valid, contradictions
    
    def validate_age_appropriate_conditions(self, specialty: str, age: int, severity: str) -> Tuple[bool, List[str]]:
        """
        Validate that the specialty and severity are age-appropriate.
        
        Args:
            specialty (str): Medical specialty
            age (int): Patient age
            severity (str): Symptom severity
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_warnings)
        """
        warnings = []
        
        if not (0 <= age <= 120):
            return False, [f"Invalid age: {age}. Must be between 0 and 120."]
        
        # Get age group
        age_group = self._get_age_group(age)
        age_rules = self.validation_rules.get('age_appropriate_conditions', {}).get(age_group, {})
        
        if age_rules:
            common_specialties = age_rules.get('common_specialties', [])
            less_common_specialties = age_rules.get('less_common_specialties', [])
            
            if specialty in less_common_specialties:
                warnings.append(f"{specialty} is less common in {age_group} patients (age {age})")
            elif specialty not in common_specialties and common_specialties:
                warnings.append(f"{specialty} is not typically common in {age_group} patients (age {age})")
        
        # Check severity appropriateness for age
        if age < 18 and severity == 'severe':
            warnings.append("Severe symptoms in pediatric patients require careful consideration")
        elif age > 80 and severity == 'mild':
            warnings.append("Mild symptoms in elderly patients may mask serious conditions")
        
        logger.debug(f"Age appropriateness validation for age {age}, specialty {specialty}: {len(warnings)} warnings")
        return True, warnings
    
    def validate_severity_symptom_compatibility(self, severity: str, symptoms: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate that the severity level is compatible with the selected symptoms.
        
        Args:
            severity (str): Severity level (mild, moderate, severe)
            symptoms (List[str]): List of symptoms
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_warnings)
        """
        warnings = []
        
        if severity not in self.severity_descriptions:
            return False, [f"Invalid severity level: {severity}. Valid options: {', '.join(self.severity_descriptions.keys())}"]
        
        severity_rules = self.validation_rules.get('severity_symptom_compatibility', {}).get(severity, {})
        
        if severity_rules:
            compatible_symptoms = severity_rules.get('compatible_symptoms', [])
            incompatible_symptoms = severity_rules.get('incompatible_symptoms', [])
            
            # This is a simplified check - in practice, you'd need more sophisticated logic
            # For now, we'll just warn about potential incompatibilities
            
            for symptom in symptoms:
                symptom_data = self.symptoms.get(symptom, {})
                severity_impact = symptom_data.get('severity_impact', {})
                
                if severity in severity_impact:
                    # Symptom has specific impact description for this severity - good
                    continue
                else:
                    warnings.append(f"Symptom '{symptom}' may not be well-defined for {severity} severity")
        
        logger.debug(f"Severity-symptom compatibility validation: {len(warnings)} warnings")
        return True, warnings
    
    def _get_age_group(self, age: int) -> str:
        """
        Determine age group based on age.
        
        Args:
            age (int): Patient age
            
        Returns:
            str: Age group name
        """
        if age < 18:
            return 'pediatric'
        elif age < 40:
            return 'young_adult'
        elif age < 65:
            return 'middle_aged'
        else:
            return 'elderly'
    
    def comprehensive_validation(self, specialty: str, symptoms: List[str], age: int, 
                                gender: str, severity: str) -> Dict[str, Any]:
        """
        Perform comprehensive validation of all patient case parameters.
        
        Args:
            specialty (str): Medical specialty
            symptoms (List[str]): List of symptoms
            age (int): Patient age
            gender (str): Patient gender
            severity (str): Symptom severity
            
        Returns:
            Dict containing validation results
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # 1. Basic validation
        basic_valid, basic_errors = self.validate_specialty(specialty)
        if not basic_valid:
            validation_result['errors'].extend(basic_errors)
            validation_result['is_valid'] = False
        
        symptoms_valid, symptom_errors = self.validate_symptoms(symptoms)
        if not symptoms_valid:
            validation_result['errors'].extend(symptom_errors)
            validation_result['is_valid'] = False
        
        # 2. Symptom-specialty compatibility
        if basic_valid and symptoms_valid:
            combo_valid, combo_messages = self.validate_symptom_specialty_combination(specialty, symptoms)
            if not combo_valid:
                validation_result['is_valid'] = False
            
            # Separate errors from warnings
            for msg in combo_messages:
                if any(word in msg.lower() for word in ['contraindicated', 'too few', 'too many']):
                    validation_result['errors'].append(msg)
                else:
                    validation_result['warnings'].append(msg)
        
        # 3. Contradictory symptoms check
        if symptoms_valid:
            contradictory_valid, contradictions = self.check_contradictory_symptoms(symptoms)
            if not contradictory_valid:
                validation_result['errors'].extend(contradictions)
                validation_result['is_valid'] = False
        
        # 4. Age appropriateness
        age_valid, age_warnings = self.validate_age_appropriate_conditions(specialty, age, severity)
        if not age_valid:
            validation_result['errors'].extend(age_warnings)
            validation_result['is_valid'] = False
        else:
            validation_result['warnings'].extend(age_warnings)
        
        # 5. Severity-symptom compatibility
        severity_valid, severity_warnings = self.validate_severity_symptom_compatibility(severity, symptoms)
        if not severity_valid:
            validation_result['errors'].extend(severity_warnings)
            validation_result['is_valid'] = False
        else:
            validation_result['warnings'].extend(severity_warnings)
        
        # 6. Generate recommendations
        validation_result['recommendations'] = self._generate_recommendations(
            specialty, symptoms, age, gender, severity, validation_result
        )
        
        logger.info(f"Comprehensive validation completed: {validation_result['is_valid']}")
        return validation_result
    
    def _generate_recommendations(self, specialty: str, symptoms: List[str], age: int, 
                                 gender: str, severity: str, validation_result: Dict) -> List[str]:
        """
        Generate recommendations based on validation results.
        
        Args:
            specialty (str): Medical specialty
            symptoms (List[str]): List of symptoms
            age (int): Patient age
            gender (str): Patient gender
            severity (str): Symptom severity
            validation_result (Dict): Current validation results
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        # If there are errors, recommend fixes
        if validation_result['errors']:
            recommendations.append("Please address all errors before proceeding with case generation")
        
        # Recommend additional symptoms if too few
        specialty_rules = self.validation_rules.get('symptom_specialty_combinations', {}).get(specialty, {})
        if specialty_rules:
            required_symptoms = specialty_rules.get('required_symptoms', [])
            missing_required = [s for s in required_symptoms if s not in symptoms]
            if missing_required:
                recommendations.append(f"Consider adding typical {specialty} symptoms: {', '.join(missing_required[:3])}")
        
        # Age-specific recommendations
        age_group = self._get_age_group(age)
        if age_group == 'elderly' and severity == 'mild':
            recommendations.append("Consider that elderly patients may present with atypical symptoms")
        elif age_group == 'pediatric':
            recommendations.append("Ensure symptoms are age-appropriate for pediatric presentation")
        
        # Severity recommendations
        if severity == 'severe' and len(symptoms) < 3:
            recommendations.append("Severe cases typically present with multiple symptoms")
        
        return recommendations
    
    def get_available_symptoms_for_specialty(self, specialty: str) -> Dict[str, List[str]]:
        """
        Get symptoms categorized by their appropriateness for a specialty.
        
        Args:
            specialty (str): Medical specialty
            
        Returns:
            Dict with 'required', 'optional', and 'contraindicated' symptom lists
        """
        specialty_rules = self.validation_rules.get('symptom_specialty_combinations', {}).get(specialty, {})
        
        return {
            'required': specialty_rules.get('required_symptoms', []),
            'optional': specialty_rules.get('optional_symptoms', []),
            'contraindicated': specialty_rules.get('contraindicated_symptoms', [])
        }
    
    def get_specialty_info(self, specialty: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a specialty.
        
        Args:
            specialty (str): Medical specialty
            
        Returns:
            Dict containing specialty information
        """
        if specialty not in self.specialties:
            return {}
        
        specialty_data = self.specialties[specialty].copy()
        specialty_data['available_symptoms'] = self.get_available_symptoms_for_specialty(specialty)
        specialty_data['validation_rules'] = self.validation_rules.get('symptom_specialty_combinations', {}).get(specialty, {})
        
        return specialty_data
    
    def get_all_specialties(self) -> Dict[str, str]:
        """
        Get all available specialties with their names.
        
        Returns:
            Dict mapping specialty keys to display names
        """
        return {key: data.get('name', key) for key, data in self.specialties.items()}
    
    def get_all_symptoms(self) -> Dict[str, str]:
        """
        Get all available symptoms with their display names.
        
        Returns:
            Dict mapping symptom keys to display names
        """
        return {key: data.get('name', key) for key, data in self.symptoms.items()}
    
    def get_severity_descriptions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all severity level descriptions.
        
        Returns:
            Dict containing severity descriptions
        """
        return self.severity_descriptions.copy()


# Convenience functions for backward compatibility
def validate_symptom_specialty_combination(specialty: str, symptoms: List[str]) -> Tuple[bool, List[str]]:
    """Backward compatibility function"""
    validator = MedicalValidationSystem()
    return validator.validate_symptom_specialty_combination(specialty, symptoms)

def validate_demographics_for_specialty(specialty: str, age: int, gender: str) -> Tuple[bool, List[str]]:
    """Backward compatibility function"""
    validator = MedicalValidationSystem()
    age_valid, age_warnings = validator.validate_age_appropriate_conditions(specialty, age, 'moderate')
    return age_valid, age_warnings

def get_available_symptoms_for_specialty(specialty: str) -> List[str]:
    """Backward compatibility function"""
    validator = MedicalValidationSystem()
    symptoms_dict = validator.get_available_symptoms_for_specialty(specialty)
    return symptoms_dict.get('required', []) + symptoms_dict.get('optional', [])

def get_specialty_info(specialty: str) -> Dict:
    """Backward compatibility function"""
    validator = MedicalValidationSystem()
    return validator.get_specialty_info(specialty)

def get_all_specialties() -> Dict:
    """Backward compatibility function"""
    validator = MedicalValidationSystem()
    return validator.get_all_specialties()

def get_all_symptoms() -> Dict:
    """Backward compatibility function"""
    validator = MedicalValidationSystem()
    return validator.get_all_symptoms() 