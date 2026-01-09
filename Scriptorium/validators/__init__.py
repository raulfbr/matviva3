# Validadores Pedagógicos

"""
Módulo de validadores para conformidade pedagógica.
- charlotte_mason: Valida "livros vivos" vs "twaddle"
- singapore_cpa: Valida progressão Concreto-Pictórico-Abstrato
- cs_lewis: Valida estilo analógico e transposição
"""

from .charlotte_mason import validate_living_style
from .singapore_cpa import validate_cpa_compliance
from .cs_lewis import check_lewis_style

__all__ = [
    'validate_living_style',
    'validate_cpa_compliance', 
    'check_lewis_style'
]
