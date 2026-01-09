"""
Main Execution Loop
Runs the Deep Search Pedagogical Architecture.
"""

import sys
import os

# Ensure we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Scriptorium.adk.core import Session, MockModel
from Scriptorium.adk.providers import GeminiProvider, OpenRouterProvider
from Scriptorium.agents import supervisor

def load_keys():
    # Priority 1: OpenRouter
    try:
        or_path = os.path.join(os.path.dirname(__file__), '.openrouter_key')
        with open(or_path, 'r') as f:
            return "openrouter", f.read().strip()
    except:
        pass
    
    # Priority 2: Gemini
    try:
        gem_path = os.path.join(os.path.dirname(__file__), '.api_key')
        with open(gem_path, 'r') as f:
            return "gemini", f.read().strip()
    except:
        return None, None

def main():
    print("=== SCRIPTORIUM: PEDAGOGICAL COUNCIL ===")
    print("(Automated Mode: The Council is Ready)")
    
    # Init Provider
    provider_type, api_key = load_keys()
    
    if not api_key:
        print("[WARNING] No API Key found (checked .openrouter_key and .api_key). Using MOCK.")
        provider = MockModel()
    elif provider_type == "openrouter":
        print("✅ OpenRouter Connected. Model: DeepSeek V3 (Standard/Stable)")
        provider = OpenRouterProvider(api_key, model_name="deepseek/deepseek-chat")
    else:
        print("✅ Gemini 3.0 Flash Connected.")
        provider = GeminiProvider(api_key, model_name="gemini-3-flash-preview")

    # DIRECT TO COUNCIL (No Choice)
    council = supervisor.Council(provider)
    session = Session()

    print("\n[The Council is seated: Mason, Singapore, Lewis, and the Headmaster.]")
    print("Tell us your topic (e.g. 'Fractions', 'Leaves', 'Courage'). Type 'exit' to quit.")

    while True:
        user_input = input("\nTopic> ").strip()
        
        if user_input.lower() == 'exit':
            break
            
        # Run Council Flow
        try:
            response = council.run_session(user_input, session)
            print(f"\n{response}")
        except Exception as e:
            print(f"\n[ERROR] Council execution failed: {e}")
            # Optional: import traceback; traceback.print_exc()

if __name__ == "__main__":
    main()
