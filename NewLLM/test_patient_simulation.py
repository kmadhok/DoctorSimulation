import unittest
import json
import os
from utils.patient_simulation import load_patient_simulation, format_patient_prompt, get_patient_system_prompt

class TestPatientSimulation(unittest.TestCase):
    def setUp(self):
        # Create a test patient simulation file
        self.test_data = {
            "prompt_template": "You are a virtual patient in a clinical simulation. You have been assigned the following profile:\n\n  • Age: {age}\n  • Gender: {gender}\n  • Occupation: {occupation}\n  • Relevant medical history: {medical_history}\n  • Underlying illness: {illness}\n  • Any recent events or exposures: {recent_exposure}\n\nYour task:\nWhen the \"Doctor\" asks you questions, respond as a real patient would.",
            "patient_details": {
                "age": "45",
                "gender": "Female",
                "occupation": "Office manager",
                "medical_history": "Hypertension, controlled with medication",
                "illness": "Migraine",
                "recent_exposure": "Working long hours with poor lighting"
            }
        }
        
        # Write test data to a temporary file
        with open('test_patient.json', 'w') as f:
            json.dump(self.test_data, f)
    
    def tearDown(self):
        # Clean up test file
        if os.path.exists('test_patient.json'):
            os.remove('test_patient.json')
    
    def test_load_patient_simulation(self):
        """Test loading patient simulation data from file"""
        data = load_patient_simulation('test_patient.json')
        self.assertEqual(data, self.test_data)
    
    def test_format_patient_prompt(self):
        """Test formatting patient prompt with details"""
        formatted = format_patient_prompt(self.test_data)
        self.assertIn("45", formatted)
        self.assertIn("Female", formatted)
        self.assertIn("Office manager", formatted)
        self.assertIn("Hypertension", formatted)
        self.assertIn("Migraine", formatted)
        self.assertIn("Working long hours", formatted)
    
    def test_get_patient_system_prompt(self):
        """Test getting system prompt from patient data"""
        prompt = get_patient_system_prompt(self.test_data)
        self.assertIn("45", prompt)
        self.assertIn("Female", prompt)
        self.assertIn("Office manager", prompt)

if __name__ == '__main__':
    unittest.main() 