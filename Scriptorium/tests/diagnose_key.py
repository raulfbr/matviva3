import requests
import os

def load_api_key():
    try:
        key_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.api_key')
        with open(key_path, 'r') as f:
            return f.read().strip()
    except:
        return None

def list_models():
    api_key = load_api_key()
    if not api_key:
        print("No API Key found.")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("Available Models:")
            for m in models:
                if 'generateContent' in m['supportedGenerationMethods']:
                    print(f"- {m['name']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    list_models()
