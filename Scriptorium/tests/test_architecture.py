"""
Test Architecture
Verifies that the Custom ADK, Tools, and Agents are wired correctly.
"""

import sys
import os
import unittest

# Ensure imports work (Add Project Root to Path)
# .../Scriptorium/tests/test_architecture.py -> .../Scriptorium/tests -> .../Scriptorium -> .../
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Scriptorium.adk.core import Agent, MockModel, Session
from Scriptorium.adk import tools
from Scriptorium.agents import definitions

class TestPedagogicalArchitecture(unittest.TestCase):
    
    def test_mason_agent_creation(self):
        agent = definitions.create_mason_agent()
        self.assertEqual(agent.name, "charlotte_mason")
        self.assertTrue("pelo menos, acender um fogo" in agent.instruction or "acender um fogo" in agent.instruction)
        
    def test_singapore_validator_tool(self):
        # Allow concrete terms
        res = tools.validate_singapore_phase("Imagine três maçãs.", "CONCRETE")
        self.assertTrue(res['is_compliant'])
        
        # Disallow digits in concrete phase
        res_bad = tools.validate_singapore_phase("3 + 2 = 5", "CONCRETE")
        self.assertFalse(res_bad['is_compliant'])
        self.assertTrue("Dígitos" in res_bad['violations'][0])

    def test_session_state_injection(self):
        agent = definitions.create_singapore_agent()
        session = Session()
        session.state['phase'] = 'PICTORIAL'
        
        # Mock model just echoes instruction, check if 'PICTORIAL' is inside
        # Actually our MockModel returns a fixed string based on prompt/instruction
        # But we can verify agent.run doesn't crash
        response = agent.run("Draw a model", session)
        self.assertIn("[MOCK OUTPUT]", response)
        self.assertEqual(session.get_last_user_message(), "Draw a model")

    def test_render_bar_model(self):
        ascii_art = tools.render_bar_model(3, 2, 5)
        self.assertIn("Total: 5", ascii_art)
        self.assertIn("|", ascii_art)


if __name__ == '__main__':
    unittest.main()
