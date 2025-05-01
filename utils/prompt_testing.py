from dataclasses import dataclass
from typing import List, Dict, Optional
import json
from datetime import datetime
import os
from .groq_integration import get_groq_response

@dataclass
class TestCase:
    """Represents a single test case with question and expected answer."""
    question: str
    expected_answer: str
    context: Optional[Dict] = None

@dataclass
class PromptTemplate:
    """Represents a prompt template with system instruction and patient profile."""
    system_instruction: str
    patient_profile: str
    name: str  # Name of the template for identification

class PromptTester:
    """Class to handle prompt testing and evaluation."""
    
    def __init__(self, model: str = "llama3-8b-8192"):
        self.model = model
        self.results_dir = "prompt_test_results"
        os.makedirs(self.results_dir, exist_ok=True)
    
    def _format_prompt(self, template: PromptTemplate, question: str) -> str:
        """Format the complete prompt with template and question."""
        return f"""Patient Profile:
{template.patient_profile}

Question: {question}"""
    
    def run_test_case(self, template: PromptTemplate, test_case: TestCase) -> Dict:
        """Run a single test case and return the results."""
        prompt = self._format_prompt(template, test_case.question)
        
        response = get_groq_response(
            input_text=prompt,
            model=self.model,
            system_prompt=template.system_instruction
        )
        
        return {
            "template_name": template.name,
            "question": test_case.question,
            "expected_answer": test_case.expected_answer,
            "actual_response": response,
            "context": test_case.context
        }
    
    def run_test_suite(self, template: PromptTemplate, test_cases: List[TestCase]) -> List[Dict]:
        """Run a suite of test cases for a given template."""
        results = []
        for test_case in test_cases:
            result = self.run_test_case(template, test_case)
            results.append(result)
        return results
    
    def save_results(self, results: List[Dict], template_name: str):
        """Save test results to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.results_dir}/{template_name}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filename

# Example usage
if __name__ == "__main__":
    # Example test cases
    test_cases = [
        TestCase(
            question="What are the key symptoms to look for in this patient?",
            expected_answer="Fever, cough, and shortness of breath",
            context={"severity": "moderate"}
        ),
        TestCase(
            question="What is the recommended treatment plan?",
            expected_answer="Rest, hydration, and over-the-counter fever reducers",
            context={"age": 45}
        )
    ]
    
    # Example template
    template = PromptTemplate(
        name="general_medical_advice",
        system_instruction="""You are a medical AI assistant. Provide clear, concise, 
        and accurate medical advice based on the patient profile and questions. 
        Always prioritize patient safety and recommend professional medical consultation 
        when necessary.""",
        patient_profile="""Patient is a 45-year-old male presenting with flu-like symptoms 
        for the past 3 days. No underlying health conditions. Vital signs are stable."""
    )
    
    # Run tests
    tester = PromptTester()
    results = tester.run_test_suite(template, test_cases)
    saved_file = tester.save_results(results, template.name)
    print(f"Test results saved to: {saved_file}") 