import os
import urllib.request
import shutil

# Define the model URL and target directory
MODEL_URL = 'https://github.com/ricky0123/vad/raw/master/public/silero_vad.onnx'
MODEL_DIR = os.path.join('static', 'models', 'vad')
MODEL_PATH = os.path.join(MODEL_DIR, 'silero_vad.onnx')

def download_vad_model():
    """Download the Silero VAD model file"""
    print(f"Downloading Silero VAD model to {MODEL_PATH}...")
    
    # Create directory if it doesn't exist
    if not os.path.exists(MODEL_DIR):
        print(f"Creating directory: {MODEL_DIR}")
        os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Download the file
    try:
        with urllib.request.urlopen(MODEL_URL) as response, open(MODEL_PATH, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("Model downloaded successfully")
        return True
    except Exception as e:
        print(f"Error downloading model: {e}")
        return False

if __name__ == "__main__":
    download_vad_model() 