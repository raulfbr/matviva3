"""
ADK Tools - Wrappers for Pedagogical Validators
Exposes the validators in `WorkFlow/validators` as ADK-compatible tools.
"""

import sys
import os

# Ensure we can import from the validators directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from validators import charlotte_mason
from validators import singapore_cpa
from validators import cs_lewis
from typing import Dict, Any

def validate_mason_style(text: str) -> Dict[str, Any]:
    """
    Validates if the text follows Charlotte Mason's 'Living Book' principles.
    Checks for: Bullet points (forbidden), Narrative Density, Twaddle.
    """
    return charlotte_mason.validate_living_style(text)

def validate_singapore_phase(text: str, phase: str) -> Dict[str, Any]:
    """
    Validates if the text adheres to the specific Singapore Math CPA phase.
    Args:
        text: The explanation text.
        phase: 'CONCRETE', 'PICTORIAL', or 'ABSTRACT'.
    """
    return singapore_cpa.validate_cpa_compliance(text, phase)

def validate_lewis_style(text: str) -> Dict[str, Any]:
    """
    Validates if the text follows C.S. Lewis's apologetic style.
    Checks for: Analogies, Humility markers, Logical flow.
    """
    # Using generic corpus for now; ideally loaded from a file
    return cs_lewis.check_lewis_style(text)

def render_bar_model(part_a: int, part_b: int, total: int = None) -> str:
    """
    Generates a text-based (ASCII) Singapore Bar Model.
    This is a 'Generative Tool' for the PICTORIAL phase.
    """
    total = total or (part_a + part_b)
    
    # Scale for ASCII representation (max width 40 chars)
    scale_factor = 40 / total if total > 0 else 1
    width_a = int(part_a * scale_factor)
    width_b = int(part_b * scale_factor)
    
    model = []
    model.append(f"Total: {total}")
    model.append("+" + "-" * (width_a + width_b) + "+")
    model.append("|" + " " * width_a + "|" + " " * width_b + "|")
    model.append("|" + f"{part_a:^{width_a}}" + "|" + f"{part_b:^{width_b}}" + "|")
    model.append("+" + "-" * (width_a + width_b) + "+")
    
    return "\n".join(model)
