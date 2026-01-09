"""
TEST SCRIPT for DeepSeek V3.2 Speciale
Checks if the model responds within a reasonable time for a small prompt.
"""
import os
import sys
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Scriptorium.adk.providers import OpenRouterProvider

def main():
    print("=== DEEPSEEK V3.2 SPECIALE LATENCY TEST ===")
    
    # Path to key
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    key_path = os.path.join(base_dir, "Scriptorium", ".openrouter_key")
    with open(key_path, 'r') as f:
        api_key = f.read().strip()

    # Use the precise model ID from the user's log
    # But generic alias is safer if provider changes. Let's use the one User confirmed.
    # User log says: "deepseek/deepseek-v3.2-speciale-20251201"
    # We will try the generic alias first, as it usually maps to latest.
    model_name = "deepseek/deepseek-v3.2-speciale"
    
    print(f"Model: {model_name}")
    provider = OpenRouterProvider(api_key, model_name=model_name)
    
    start_time = time.time()
    print("\nSending prompt: 'Explain the concept of 'Living Ideas' in 1 sentence.'...")
    
    try:
        # We assume providers.py has the infinite timeout now? Not yet.
        # But this is a short prompt, should be fast.
        response = provider.generate("Explain 'Living Ideas' (Charlotte Mason) in one short sentence.")
        
        duration = time.time() - start_time
        print(f"\n✅ RESPONSE RECEIVED in {duration:.2f}s:")
        print(f"'{response}'")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
