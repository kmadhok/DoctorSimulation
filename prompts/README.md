# Prompts Directory

This directory contains all prompt-related files for the Doctor Simulation project.

## Directory Structure

```
prompts/
├── templates/         # Contains prompt templates in markdown format
├── test_cases/       # Contains test cases and example prompts
└── results/          # Contains generated results from prompt testing
```

## Files

### Templates
- `patient_simulation.md`: Main template for patient simulation scenarios
- `example_prompts.json`: Example prompts for testing

### Test Cases
- Test cases and example prompts for different scenarios

### Results
- Generated JSON files from prompt testing and patient simulations
- Files are automatically named with timestamps

## Usage

1. To use a prompt template:
   ```python
   from utils.prompt_testing import load_markdown_prompt
   
   template = load_markdown_prompt("prompts/templates/patient_simulation.md")
   ```

2. To run prompt tests:
   ```bash
   python test_prompts.py --prompts-file prompts/templates/example_prompts.json
   ```

3. To run patient simulation:
   ```bash
   python test_prompts.py --patient-simulation --prompt-template prompts/templates/patient_simulation.md
   ``` 