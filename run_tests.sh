#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Running Doctor Simulation Tests..."
echo "================================"

# Run Python tests
echo -e "\n${GREEN}Running Python Tests...${NC}"
python -m pytest tests/test_audio_recording.py -v
PYTHON_RESULT=$?

# Run JavaScript tests
echo -e "\n${GREEN}Running JavaScript Tests...${NC}"
npm test
JS_RESULT=$?

# Check if both test suites passed
if [ $PYTHON_RESULT -eq 0 ] && [ $JS_RESULT -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed!${NC}"
    exit 1
fi