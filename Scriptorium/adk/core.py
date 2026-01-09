"""
ADK Core - Lightweight Agent Development Kit
Mimics the Google ADK interface for pedagogical agent orchestration.
"""

from typing import List, Dict, Any, Callable, Optional, Union
import uuid
from dataclasses import dataclass, field
import inspect

@dataclass
class Session:
    """
    Manages the state of a conversation session.
    Equivalent to ctx.session in standard ADK.
    """
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    history: List[Dict[str, str]] = field(default_factory=list)
    state: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_last_user_message(self) -> Optional[str]:
        for msg in reversed(self.history):
            if msg["role"] == "user":
                return msg["content"]
        return None

    def get_last_model_message(self) -> Optional[str]:
        for msg in reversed(self.history):
            if msg["role"] == "model":
                return msg["content"]
        return None

    def get_history_text(self) -> str:
        """
        Returns the full conversation history formatted as a string.
        """
        text = ""
        for msg in self.history:
            role = "User" if msg["role"] == "user" else "Assistant"
            text += f"{role}: {msg['content']}\n"
        return text

class Model:
    """
    Abstract base class for LLM backends.
    """
    def generate(self, prompt: str, system_instruction: str = None) -> str:
        raise NotImplementedError

class MockModel(Model):
    """
    A mock model for testing purposes without API keys.
    """
    def generate(self, prompt: str, system_instruction: str = None) -> str:
        return f"[MOCK OUTPUT] Based on instruction '{system_instruction[:20]}...', I respond to: {prompt[:20]}..."

class Agent:
    """
    Represents a pedagogical agent with a specific persona and constraints.
    """
    def __init__(
        self, 
        name: str, 
        instruction: str, 
        model: Model,
        tools: List[Callable] = None
    ):
        self.name = name
        self.instruction = instruction
        self.model = model
        self.tools = tools or []
        self._tool_map = {t.__name__: t for t in self.tools}

    def run(self, input_text: str, session: Session) -> str:
        """
        Executes a turn:
        1. Contextualize instruction with session state.
        2. call Model.
        3. (Optional) Tool execution logic could go here, but for this architecture,
           we are using tools primarily for *post-generation validation* or *explicit use*.
        """
        # 1. Update Session
        session.add_message("user", input_text)
        
        # 2. Format Instruction (Dynamic Context)
        # Safe formatting considering session state might not have all keys
        try:
            formatted_instruction = self.instruction.format(**session.state)
        except KeyError:
            formatted_instruction = self.instruction  # Fallback if keys missing

        # 3. Generate
        full_prompt = session.get_history_text() + f"\nUser: {input_text}\nAssistant:"
        response_text = self.model.generate(full_prompt, system_instruction=formatted_instruction)
        
        # 4. Save to History
        # session.add_message("model", response_text) # Don't save yet if retrying? Actually run() usually saves. 
        # But for retry loop we might want to be careful. For now, standard run saves.
        session.add_message("model", response_text)
        
        return response_text

    def run_with_retry(self, input_text: str, session: Session, validator_func_name: str, max_retries: int = 2) -> str:
        """
        Executes the agent with an automatic feedback loop.
        If validation fails, it feeds the errors back to the model and retries.
        """
        print(f"  [Auto-Refinement] Attempt 1/{max_retries+1}...")
        response = self.run(input_text, session)
        
        for i in range(max_retries):
            # Validate
            # We need to find the tool function by name. 
            # In a real ADK this is cleaner. Here we iterate our tools list.
            validator = next((t for t in self.tools if t.__name__ == validator_func_name), None)
            
            if not validator:
                return response # Cannot validate
            
            # Execute Validator
            # We assume the validator takes (text) or (text, phase)
            # This is a bit hacky for the dynamic arguments, but fits our current scope.
            try:
                if 'phase' in inspect.signature(validator).parameters:
                   valid_result = validator(response, phase=session.state.get('phase', 'CONCRETE'))
                else:
                   valid_result = validator(response)
            except Exception as e:
                print(f"  [Validator Error]: {e}")
                return response

            if valid_result.get('is_compliant', False):
                print(f"  [✅ Validated] Score: {valid_result.get('score', 'N/A')}")
                return response
            
            # If we are here, it failed.
            feedback = valid_result.get('feedback', 'Validation failed.')
            if isinstance(feedback, list): feedback = "; ".join(feedback)
            violations = valid_result.get('violations', [])
            if violations: feedback += "; ".join(violations)

            print(f"  [⚠️ Violation] {feedback}")
            print(f"  [Auto-Refinement] Retrying ({i+1}/{max_retries})...")
            
            # Add critique to session as a "System" or "User" injection to guide the fix
            critique_prompt = f"SYSTEM: A sua resposta anterior violou as regras pedagógicas. Feedback do Supervisor: [{feedback}]. Corrija a resposta imediatamente."
            # We inject this into the flow.
            response = self.run(critique_prompt, session)
            
        return response

    def validate_last_response(self, session: Session, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Explicitly calls a validation tool on the last model response.
        """
        last_response = session.get_last_model_message()
        if not last_response:
            return {"error": "No response to validate"}
            
        tool = self._tool_map.get(tool_name)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found in agent {self.name}")

        # Automatically inject 'text' or 'response' arguments if needed
        # This is a simple dependency injection for the validator
        sig = inspect.signature(tool)
        call_args = kwargs.copy()
        
        if 'text' in sig.parameters and 'text' not in call_args:
            call_args['text'] = last_response
            
        return tool(**call_args)
