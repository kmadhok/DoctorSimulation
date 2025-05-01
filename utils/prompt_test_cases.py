from typing import List
from .prompt_testing import TestCase, PromptTemplate

# Test Cases for General Medical Assessment
GENERAL_MEDICAL_TEST_CASES: List[TestCase] = [
    TestCase(
        question="What are the primary symptoms to monitor in this patient?",
        expected_answer="Fever, cough, and respiratory rate",
        context={"condition": "respiratory"}
    ),
    TestCase(
        question="What are the recommended next steps for this patient?",
        expected_answer="Schedule follow-up appointment and monitor symptoms",
        context={"severity": "mild"}
    ),
    TestCase(
        question="What medications should be avoided given the patient's history?",
        expected_answer="NSAIDs due to history of gastric ulcers",
        context={"allergies": ["aspirin", "ibuprofen"]}
    )
]

# Test Cases for Emergency Response
EMERGENCY_TEST_CASES: List[TestCase] = [
    TestCase(
        question="What immediate actions should be taken?",
        expected_answer="Call emergency services and monitor vital signs",
        context={"situation": "acute"}
    ),
    TestCase(
        question="What are the critical signs to watch for?",
        expected_answer="Changes in consciousness, breathing difficulty, severe pain",
        context={"urgency": "high"}
    )
]

# Test Cases for Chronic Condition Management
CHRONIC_CONDITION_TEST_CASES: List[TestCase] = [
    TestCase(
        question="What lifestyle modifications are recommended?",
        expected_answer="Regular exercise, balanced diet, and stress management",
        context={"condition": "diabetes"}
    ),
    TestCase(
        question="How should medication adherence be monitored?",
        expected_answer="Daily pill organizer and regular follow-ups",
        context={"medication": "multiple"}
    )
]

# Prompt Templates
GENERAL_MEDICAL_TEMPLATE = PromptTemplate(
    name="general_medical_assessment",
    system_instruction="""You are a medical AI assistant specializing in general medical assessment.
    Provide clear, evidence-based responses focusing on:
    1. Symptom assessment
    2. Risk factors
    3. Recommended next steps
    Always emphasize the importance of professional medical consultation.""",
    patient_profile="""45-year-old male with history of hypertension.
    Presenting with flu-like symptoms for 3 days.
    No known allergies. Current medications: Lisinopril 10mg daily."""
)

EMERGENCY_TEMPLATE = PromptTemplate(
    name="emergency_response",
    system_instruction="""You are an emergency medical AI assistant.
    Focus on:
    1. Immediate action steps
    2. Critical signs to monitor
    3. When to seek emergency care
    Always prioritize patient safety and immediate medical attention when necessary.""",
    patient_profile="""60-year-old female with history of heart disease.
    Experiencing chest pain and shortness of breath.
    Current medications: Aspirin 81mg, Metoprolol 50mg."""
)

CHRONIC_CONDITION_TEMPLATE = PromptTemplate(
    name="chronic_condition_management",
    system_instruction="""You are a chronic disease management AI assistant.
    Focus on:
    1. Long-term management strategies
    2. Lifestyle modifications
    3. Medication adherence
    4. Regular monitoring parameters
    Emphasize the importance of consistent care and regular follow-ups.""",
    patient_profile="""55-year-old male with Type 2 Diabetes.
    Diagnosed 5 years ago. HbA1c: 7.2%.
    Current medications: Metformin 1000mg twice daily, Glipizide 5mg daily."""
)

# Function to get all test cases and templates
def get_all_test_cases() -> List[TestCase]:
    """Return all test cases combined."""
    return (
        GENERAL_MEDICAL_TEST_CASES +
        EMERGENCY_TEST_CASES +
        CHRONIC_CONDITION_TEST_CASES
    )

def get_all_templates() -> List[PromptTemplate]:
    """Return all prompt templates."""
    return [
        GENERAL_MEDICAL_TEMPLATE,
        EMERGENCY_TEMPLATE,
        CHRONIC_CONDITION_TEMPLATE
    ] 