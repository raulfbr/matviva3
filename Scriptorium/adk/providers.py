"""
ADK Providers - LLM Backends
Implements the connection to Real LLMs (Gemini).
"""

import requests
import json
from .core import Model

class GeminiProvider(Model):
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        """
        Calls Gemini API.
        Note: System Instruction in Gemini API is passed differently (in 'system_instruction' field),
        but for simple consistency with the 'generate' interface, we can prepend it or use the proper field if the API version supports it.
        v1beta supports system_instruction.
        """
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                # "maxOutputTokens": 800,
            }
        }

        # Inject system instruction if present
        if system_instruction:
            data["system_instruction"] = {
                "parts": [{"text": system_instruction}]
            }

        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                data=json.dumps(data)
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Parse response
            try:
                return result['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError) as e:
                return f"[ERROR parsing Gemini response]: {result}"

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                return "**[ALERTA DE COTA]** 🛑 A API atingiu o limite de requisições (Quota Exceeded). Por favor, aguarde ou troque a API Key em '.api_key'."
            return f"[API ERROR {response.status_code}]: {response.text}"
        except requests.exceptions.RequestException as e:
            return f"[API CONNECTION ERROR]: {str(e)}"

class OpenRouterProvider(Model):
    def __init__(self, api_key: str, model_name: str = "deepseek/deepseek-v3.2-speciale"):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://scriptorium.local", # Required by OpenRouter
            "X-Title": "Scriptorium Pedagogy"
        }
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            # "max_tokens": 4000
        }

        try:
            # Timeout set to 5 minutes (300s) because DeepSeek Speciale takes time to "think".
            response = requests.post(self.base_url, headers=headers, data=json.dumps(data), timeout=300)
            
            if response.status_code == 429:
                 return "**[ALERTA DE COTA]** 🛑 A API do OpenRouter atingiu o limite (Rate Limit). Tente novamente."
            
            if response.status_code == 402:
                 return "**[SALDO INSUFICIENTE]** 🛑 Seus créditos no OpenRouter acabaram. Por favor, recarregue em openrouter.ai/credits."

            response.raise_for_status()
            result = response.json()
            
            try:
                return result['choices'][0]['message']['content']
            except (KeyError, IndexError):
                return f"[ERROR parsing OpenRouter response]: {result}"

        except requests.exceptions.RequestException as e:
             return f"[API CONNECTION ERROR]: {str(e)}"
