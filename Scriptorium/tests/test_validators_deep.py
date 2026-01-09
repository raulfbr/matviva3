"""
Test Validators Deep rEALISM
Runs specific realistic examples through the validators to verify
they correctly accept high-quality text and reject low-quality text.
"""

import sys
import os
import unittest

# Ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from WorkFlow.adk import tools
from WorkFlow.tests import data_corpus

class TestValidatorsDeep(unittest.TestCase):

    # --- CHARLOTTE MASON TESTS ---
    
    def test_mason_accepts_good_narrative(self):
        result = tools.validate_mason_style(data_corpus.MASON_COMPLIANT)
        self.assertTrue(result['is_compliant'])
        self.assertEqual(result['metrics']['has_bullet_points'], False)
        # Should have good readability grade (above 5.0 usually, or close to it depending on calc)
        # Our mock calc might be simple, but let's check input
        print(f"\n[MASON GOOD] Score: {result['score']}")

    def test_mason_rejects_lists(self):
        result = tools.validate_mason_style(data_corpus.MASON_NON_COMPLIANT_LIST)
        self.assertFalse(result['is_compliant'])
        self.assertTrue(result['metrics']['has_bullet_points'])
        print(f"\n[MASON LIST] Violations: {result['feedback']}")

    def test_mason_rejects_twaddle(self):
        result = tools.validate_mason_style(data_corpus.MASON_NON_COMPLIANT_TWADDLE)
        # Twaddle detection might lower score significantly
        self.assertLess(result['score'], 80)
        self.assertTrue(any("Twaddle" in f or "twaddle" in str(result['metrics']) for f in result['feedback']))
        print(f"\n[MASON TWADDLE] Score: {result['score']}")

    # --- SINGAPORE MATH TESTS ---

    def test_singapore_concrete_compliant(self):
        result = tools.validate_singapore_phase(data_corpus.SINGAPORE_CONCRETE_COMPLIANT, "CONCRETE")
        self.assertTrue(result['is_compliant'])
        # Check if concrete nouns were detected
        self.assertTrue(len(result['detected']['concrete_nouns']) > 0)
        print(f"\n[CPA CONCRETE GOOD] Detected: {result['detected']['concrete_nouns']}")

    def test_singapore_concrete_rejects_digits(self):
        result = tools.validate_singapore_phase(data_corpus.SINGAPORE_CONCRETE_NON_COMPLIANT, "CONCRETE")
        self.assertFalse(result['is_compliant'])
        self.assertTrue(len(result['detected']['digits']) > 0)
        print(f"\n[CPA CONCRETE BAD] Violations: {result['violations']}")

    # --- C.S. LEWIS TESTS ---

    def test_lewis_accepts_analogy(self):
        result = tools.validate_lewis_style(data_corpus.LEWIS_COMPLIANT)
        self.assertTrue(result['is_compliant'])
        self.assertTrue(result['has_analogies'])
        self.assertTrue(result['has_humility'])
        print(f"\n[LEWIS GOOD] Analogies: {result['detected']['analogies']}")

    def test_lewis_rejects_technical(self):
        result = tools.validate_lewis_style(data_corpus.LEWIS_NON_COMPLIANT)
        # Should mention lack of humility or analogies
        self.assertFalse(result['is_compliant']) # Or at least score lowered
        print(f"\n[LEWIS BAD] Feedback: {result['feedback']}")

if __name__ == '__main__':
    unittest.main()
