import json
from typing import List, Dict
from datetime import datetime
import os
from .prompt_testing import PromptTester
from .prompt_test_cases import get_all_test_cases, get_all_templates

class PromptTestAnalyzer:
    """Analyzes and compares results from different prompt templates."""
    
    def __init__(self, results_dir: str = "prompt_test_results"):
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze test results and generate metrics."""
        analysis = {
            "total_tests": len(results),
            "templates_tested": set(),
            "response_lengths": [],
            "context_usage": {}
        }
        
        for result in results:
            template_name = result["template_name"]
            analysis["templates_tested"].add(template_name)
            
            # Analyze response length
            response_length = len(result["actual_response"])
            analysis["response_lengths"].append(response_length)
            
            # Analyze context usage
            if result["context"]:
                for key in result["context"]:
                    if key not in analysis["context_usage"]:
                        analysis["context_usage"][key] = 0
                    analysis["context_usage"][key] += 1
        
        # Calculate average response length
        analysis["avg_response_length"] = sum(analysis["response_lengths"]) / len(analysis["response_lengths"])
        
        return analysis
    
    def save_analysis(self, analysis: Dict, timestamp: str):
        """Save analysis results to a JSON file."""
        filename = f"{self.results_dir}/analysis_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        return filename

def main():
    # Initialize tester and analyzer
    tester = PromptTester()
    analyzer = PromptTestAnalyzer()
    
    # Get all test cases and templates
    test_cases = get_all_test_cases()
    templates = get_all_templates()
    
    # Run tests for each template
    all_results = []
    for template in templates:
        print(f"\nTesting template: {template.name}")
        results = tester.run_test_suite(template, test_cases)
        all_results.extend(results)
        
        # Save individual template results
        saved_file = tester.save_results(results, template.name)
        print(f"Results saved to: {saved_file}")
    
    # Analyze all results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    analysis = analyzer.analyze_results(all_results)
    analysis_file = analyzer.save_analysis(analysis, timestamp)
    
    # Print summary
    print("\nTest Summary:")
    print(f"Total tests run: {analysis['total_tests']}")
    print(f"Templates tested: {', '.join(analysis['templates_tested'])}")
    print(f"Average response length: {analysis['avg_response_length']:.2f} characters")
    print(f"Analysis saved to: {analysis_file}")

if __name__ == "__main__":
    main() 