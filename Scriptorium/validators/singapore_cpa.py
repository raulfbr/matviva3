"""
Validador Singapura CPA - Progressão Concreto-Pictórico-Abstrato

Garante que explicações matemáticas respeitem a fase atual:
- CONCRETE: Objetos tangíveis, sem dígitos ou símbolos
- PICTORIAL: Modelos visuais, barras, diagramas
- ABSTRACT: Notação matemática completa
"""

import re
from typing import Dict, Any, List, Literal
from enum import Enum


class CPAPhase(Enum):
    CONCRETE = "CONCRETE"
    PICTORIAL = "PICTORIAL"
    ABSTRACT = "ABSTRACT"


# Palavras concretas (objetos tangíveis) em português
CONCRETE_NOUNS = {
    'maçã', 'maçãs', 'bola', 'bolas', 'bloco', 'blocos',
    'pedra', 'pedras', 'lápis', 'caneta', 'livro', 'livros',
    'caixa', 'caixas', 'brinquedo', 'brinquedos', 'boneca', 'bonecas',
    'carro', 'carros', 'animal', 'animais', 'flor', 'flores',
    'árvore', 'árvores', 'dedo', 'dedos', 'mão', 'mãos',
    'prato', 'pratos', 'copo', 'copos', 'fruta', 'frutas',
    'moeda', 'moedas', 'botão', 'botões', 'semente', 'sementes',
    'pizza', 'pizzas', 'bolo', 'bolos', 'chocolate', 'chocolates',
    'menino', 'menina', 'criança', 'crianças', 'pessoa', 'pessoas'
}

# Termos visuais/pictóricos
PICTORIAL_TERMS = {
    'barra', 'barras', 'modelo', 'modelos', 'diagrama', 'diagramas',
    'desenho', 'desenhos', 'figura', 'figuras', 'imagem', 'imagens',
    'retângulo', 'retângulos', 'quadrado', 'quadrados', 'parte', 'partes',
    'todo', 'inteiro', 'metade', 'terço', 'quarto', 'pedaço', 'pedaços',
    'bloco', 'blocos', 'representação', 'visual', 'visualmente'
}

# Numerais por extenso (permitidos na fase concreta)
NUMERALS_BY_EXTENSION = {
    'um', 'uma', 'dois', 'duas', 'três', 'quatro', 'cinco',
    'seis', 'sete', 'oito', 'nove', 'dez', 'onze', 'doze',
    'primeiro', 'segundo', 'terceiro', 'quarto', 'quinto'
}


def _has_digits(text: str) -> List[str]:
    """Encontra dígitos numéricos no texto."""
    return re.findall(r'\d+', text)


def _has_math_symbols(text: str) -> List[str]:
    """Encontra símbolos matemáticos no texto."""
    # Exclui hífen usado em palavras compostas
    symbols = re.findall(r'[+×÷=<>≤≥±√∑∏∫]', text)
    # Detecta operações como "3-2" mas não "bem-vindo"
    operations = re.findall(r'\d\s*[-]\s*\d', text)
    return symbols + operations


def _has_concrete_nouns(text: str) -> List[str]:
    """Encontra substantivos concretos no texto."""
    words = set(re.findall(r'\b\w+\b', text.lower()))
    return list(words & CONCRETE_NOUNS)


def _has_pictorial_terms(text: str) -> List[str]:
    """Encontra termos pictóricos/visuais no texto."""
    words = set(re.findall(r'\b\w+\b', text.lower()))
    return list(words & PICTORIAL_TERMS)


def _has_action_verbs(text: str) -> bool:
    """Verifica se há verbos de ação manipulativa."""
    action_verbs = [
        r'\bjunt[aoe]', r'\bsepara', r'\btir[aoe]', r'\bcoloc[aoe]',
        r'\bmov[aoe]', r'\bpeg[aoe]', r'\bsegur[aoe]', r'\bgrupo',
        r'\bdivid[aoe]', r'\brepartir', r'\bdistribuir'
    ]
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in action_verbs)


def validate_cpa_compliance(
    text: str,
    phase: Literal["CONCRETE", "PICTORIAL", "ABSTRACT"]
) -> Dict[str, Any]:
    """
    Verifica se a resposta do agente/texto viola as restrições da fase CPA atual.
    
    Args:
        text: Texto a ser validado
        phase: Fase atual ("CONCRETE", "PICTORIAL", "ABSTRACT")
    
    Returns:
        Dict com is_compliant, violations e recommendations
    """
    violations = []
    recommendations = []
    warnings = []
    
    digits_found = _has_digits(text)
    symbols_found = _has_math_symbols(text)
    concrete_found = _has_concrete_nouns(text)
    pictorial_found = _has_pictorial_terms(text)
    has_actions = _has_action_verbs(text)
    
    if phase == "CONCRETE":
        # Regras da fase CONCRETA
        if digits_found:
            violations.append(
                f"VIOLAÇÃO: Dígitos encontrados ({', '.join(digits_found[:5])}). "
                "Use numerais por extenso (um, dois, três)."
            )
        
        if symbols_found:
            violations.append(
                f"VIOLAÇÃO: Símbolos matemáticos proibidos na fase CONCRETA."
            )
        
        if not concrete_found:
            warnings.append(
                "ALERTA: Ausência de objetos concretos. "
                "Inclua referências tangíveis (maçãs, blocos, dedos)."
            )
            recommendations.append("Adicione objetos físicos que a criança pode visualizar ou manipular.")
        
        if not has_actions:
            recommendations.append(
                "Considere usar verbos de ação (juntar, separar, tirar, colocar)."
            )
    
    elif phase == "PICTORIAL":
        # Regras da fase PICTÓRICA
        if not pictorial_found:
            violations.append(
                "VIOLAÇÃO: Fase PICTÓRICA requer referência a modelos visuais "
                "(barra, diagrama, desenho, parte/todo)."
            )
        
        # Na fase pictórica, dígitos são permitidos em contexto de modelo
        # Mas equações completas ainda são evitadas
        equation_pattern = r'\d+\s*[+\-×÷]\s*\d+\s*=\s*\d+'
        if re.search(equation_pattern, text):
            warnings.append(
                "ALERTA: Equação completa detectada. Na fase PICTÓRICA, "
                "foque nas relações visuais antes da notação final."
            )
    
    elif phase == "ABSTRACT":
        # Fase ABSTRATA - mais permissiva
        if not digits_found and not symbols_found:
            recommendations.append(
                "Fase ABSTRATA: considere usar notação matemática formal."
            )
    
    # Calcula score
    score = 100
    score -= len(violations) * 30
    score -= len(warnings) * 10
    score = max(score, 0)
    
    return {
        "is_compliant": len(violations) == 0,
        "score": score,
        "phase": phase,
        "violations": violations,
        "warnings": warnings,
        "recommendations": recommendations,
        "detected": {
            "digits": digits_found[:5] if digits_found else [],
            "symbols": symbols_found[:5] if symbols_found else [],
            "concrete_nouns": concrete_found[:5] if concrete_found else [],
            "pictorial_terms": pictorial_found[:5] if pictorial_found else [],
            "has_action_verbs": has_actions
        }
    }


# Exemplo de uso
if __name__ == "__main__":
    # Teste CONCRETO - BOM
    texto_concreto_bom = """
    Imagine que você tem três maçãs vermelhas na sua mão esquerda.
    Agora a mamãe te dá mais duas maçãs. Junte todas as maçãs.
    Quantas maçãs você está segurando agora?
    """
    
    # Teste CONCRETO - RUIM (usa dígitos)
    texto_concreto_ruim = """
    Você tem 3 maçãs. Ganha mais 2. Quanto é 3 + 2?
    """
    
    # Teste PICTÓRICO - BOM
    texto_pictorico_bom = """
    Vamos desenhar um modelo de barras. A primeira parte representa 
    as maçãs que você tinha. A segunda parte representa as maçãs 
    que ganhou. O todo mostra quantas maçãs você tem agora.
    """
    
    print("=== CONCRETO BOM ===")
    r1 = validate_cpa_compliance(texto_concreto_bom, "CONCRETE")
    print(f"Compliant: {r1['is_compliant']}, Score: {r1['score']}")
    print(f"Concretos: {r1['detected']['concrete_nouns']}")
    
    print("\n=== CONCRETO RUIM ===")
    r2 = validate_cpa_compliance(texto_concreto_ruim, "CONCRETE")
    print(f"Compliant: {r2['is_compliant']}, Score: {r2['score']}")
    print(f"Violações: {r2['violations']}")
    
    print("\n=== PICTÓRICO BOM ===")
    r3 = validate_cpa_compliance(texto_pictorico_bom, "PICTORIAL")
    print(f"Compliant: {r3['is_compliant']}, Score: {r3['score']}")
    print(f"Pictóricos: {r3['detected']['pictorial_terms']}")
