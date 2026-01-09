"""
Validador Charlotte Mason - Detecção de "Twaddle" e Qualidade Narrativa

Métricas implementadas:
1. Flesch-Kincaid Grade (complexidade textual)
2. Detecção de bullet points (proibido em "livros vivos")
3. Densidade narrativa (pronomes pessoais + verbos de ação)
4. Diversidade lexical (Type-Token Ratio)
"""

import re
from typing import Dict, Any, List

# Tentativa de importar textstat (opcional, com fallback)
try:
    import textstat
    HAS_TEXTSTAT = True
except ImportError:
    HAS_TEXTSTAT = False


# Marcadores narrativos em português
NARRATIVE_MARKERS = {
    'ele', 'ela', 'eles', 'elas', 'então', 'depois', 'antes',
    'disse', 'perguntou', 'respondeu', 'vi', 'fui', 'era', 'foi',
    'estava', 'tinha', 'havia', 'quando', 'enquanto', 'porque'
}

# Palavras "twaddle" - linguagem infantilizada/vazia
TWADDLE_PATTERNS = [
    r'\b(legal|muito legal|super legal)\b',
    r'\b(né|tá|pra gente)\b',
    r'\b(vamos aprender|vamos ver)\b',
    r'\b(fácil|facilzinho|moleza)\b',
    r'\b(criançada|galerinha|pessoal)\b',
]


def _calculate_lexical_diversity(text: str) -> float:
    """Calcula Type-Token Ratio (diversidade vocabular)."""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0.0
    unique_words = set(words)
    return len(unique_words) / len(words)


def _detect_bullet_points(text: str) -> bool:
    """Detecta se o texto contém listas ou bullet points."""
    bullet_pattern = r'^\s*[-*•▪▸►◦‣⁃\d\.]+\s+'
    return bool(re.search(bullet_pattern, text, re.MULTILINE))


def _calculate_narrative_density(text: str) -> float:
    """Calcula proporção de marcadores narrativos no texto."""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0.0
    marker_count = sum(1 for w in words if w in NARRATIVE_MARKERS)
    return marker_count / len(words)


def _detect_twaddle(text: str) -> List[str]:
    """Detecta padrões de linguagem 'twaddle' no texto."""
    found = []
    text_lower = text.lower()
    for pattern in TWADDLE_PATTERNS:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            found.extend(matches)
    return found


def validate_living_style(
    text: str,
    min_complexity: float = 5.0,
    min_narrative_density: float = 0.05,
    min_lexical_diversity: float = 0.4
) -> Dict[str, Any]:
    """
    Valida se um texto adere aos princípios de 'Livros Vivos' de Charlotte Mason.
    
    Args:
        text: Texto a ser validado
        min_complexity: Nível mínimo Flesch-Kincaid (default: 5.0)
        min_narrative_density: Densidade narrativa mínima (default: 0.05)
        min_lexical_diversity: TTR mínimo (default: 0.4)
    
    Returns:
        Dict com is_compliant, score, métricas e feedback
    """
    feedback = []
    score = 100
    
    # 1. Verificação de Estrutura (Proibição de Listas)
    has_bullets = _detect_bullet_points(text)
    if has_bullets:
        score -= 50
        feedback.append("CRÍTICO: Texto contém listas/bullet points. Use prosa narrativa contínua.")
    
    # 2. Verificação de Complexidade
    if HAS_TEXTSTAT:
        # Configura para português se disponível
        textstat.set_lang('pt')
        readability = textstat.flesch_kincaid_grade(text)
    else:
        # Fallback: estimativa baseada em comprimento médio de frase
        sentences = re.split(r'[.!?]+', text)
        words = re.findall(r'\b\w+\b', text)
        avg_words_per_sentence = len(words) / max(len(sentences), 1)
        readability = avg_words_per_sentence / 2  # Estimativa grosseira
    
    if readability < min_complexity:
        score -= 20
        feedback.append(f"ALERTA: Complexidade baixa ({readability:.1f}). Enriqueça o vocabulário.")
    
    # 3. Verificação de Densidade Narrativa
    narrative_density = _calculate_narrative_density(text)
    if narrative_density < min_narrative_density:
        score -= 10
        feedback.append(f"ALERTA: Baixa densidade narrativa ({narrative_density:.1%}). Texto muito expositivo.")
    
    # 4. Verificação de Diversidade Lexical
    lexical_diversity = _calculate_lexical_diversity(text)
    if lexical_diversity < min_lexical_diversity:
        score -= 10
        feedback.append(f"ALERTA: Baixa diversidade lexical ({lexical_diversity:.1%}). Vocabulário repetitivo.")
    
    # 5. Detecção de Twaddle
    twaddle_found = _detect_twaddle(text)
    if twaddle_found:
        score -= 15
        feedback.append(f"ALERTA: Linguagem 'twaddle' detectada: {', '.join(set(twaddle_found))}")
    
    return {
        "is_compliant": score >= 80,
        "score": max(score, 0),
        "metrics": {
            "readability_grade": round(readability, 2),
            "narrative_density": round(narrative_density, 4),
            "lexical_diversity": round(lexical_diversity, 4),
            "has_bullet_points": has_bullets,
            "twaddle_count": len(twaddle_found)
        },
        "feedback": feedback if feedback else ["OK: Texto aprovado como 'livro vivo'."]
    }


# Exemplo de uso
if __name__ == "__main__":
    # Teste com texto bom (narrativo)
    texto_bom = """
    Era uma vez um menino chamado Tomás que adorava explorar o jardim de sua avó.
    Ele passava tardes inteiras observando as formigas carregarem folhas, enquanto 
    imaginava cidades subterrâneas repletas de pequenos trabalhadores. Sua avó 
    dizia que cada formiga conhecia seu propósito, e Tomás perguntava-se se ele 
    também encontraria o seu.
    """
    
    # Teste com texto ruim (twaddle com listas)
    texto_ruim = """
    Vamos aprender sobre formigas, pessoal!
    
    - Formigas são legais
    - Elas trabalham muito
    - É muito fácil entender
    
    Super legal, né?
    """
    
    print("=== Texto Bom ===")
    resultado_bom = validate_living_style(texto_bom)
    print(f"Score: {resultado_bom['score']}")
    print(f"Compliant: {resultado_bom['is_compliant']}")
    print(f"Feedback: {resultado_bom['feedback']}")
    
    print("\n=== Texto Ruim ===")
    resultado_ruim = validate_living_style(texto_ruim)
    print(f"Score: {resultado_ruim['score']}")
    print(f"Compliant: {resultado_ruim['is_compliant']}")
    print(f"Feedback: {resultado_ruim['feedback']}")
