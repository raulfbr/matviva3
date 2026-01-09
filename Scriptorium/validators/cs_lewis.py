"""
Validador C.S. Lewis - Estilo Analógico e Transposição

Garante que textos (especialmente diálogos de Guardiões) sigam:
1. Uso de analogias e transposição
2. Tom erudito mas acessível
3. Ancoragem em experiências concretas
4. Progressão lógica de argumentos
"""

import re
from typing import Dict, Any, List
from collections import Counter

# Tentativa de importar sklearn (opcional)
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# Marcadores de analogia em português
ANALOGY_MARKERS = {
    'como', 'assim como', 'tal como', 'semelhante', 'parecido',
    'imagine', 'imagina', 'suponha', 'suponhamos', 'pense',
    'é como se', 'seria como', 'funciona como', 'lembra',
    'compare', 'comparar', 'analogia', 'metáfora',
    'por exemplo', 'digamos que', 'faz de conta'
}

# Marcadores de humildade intelectual (estilo Lewis)
HUMILITY_MARKERS = {
    'parece-me', 'parece que', 'creio', 'acredito', 'suponho',
    'talvez', 'possivelmente', 'provavelmente', 'pode ser',
    'não tenho certeza', 'arrisco dizer', 'ousaria sugerir',
    'confesso', 'admito', 'pergunto-me'
}

# Marcadores de progressão lógica
LOGICAL_MARKERS = {
    'portanto', 'logo', 'assim', 'consequentemente', 'então',
    'primeiro', 'segundo', 'terceiro', 'por fim', 'finalmente',
    'além disso', 'ademais', 'por outro lado', 'no entanto',
    'se... então', 'porque', 'pois', 'visto que', 'dado que'
}

# Corpus de referência Lewis (excertos característicos)
LEWIS_REFERENCE_CORPUS = [
    "O arrependimento não é apenas sentir-se mal. É um pouco como desaprender a tocar uma música errada para aprender a certa.",
    "Imagine que você está fazendo uma soma e percebe um erro no início. Você não pode simplesmente continuar; deve voltar atrás e corrigir.",
    "Suponha que existam dois tipos de pessoas: as que dizem a Deus 'Seja feita a Tua vontade' e aquelas a quem Deus diz 'Seja feita a tua vontade'.",
    "A humildade não é pensar menos de si mesmo, mas pensar menos em si mesmo.",
    "Se você procurar a verdade, pode encontrar o conforto no final. Se você procurar o conforto, não encontrará nem o conforto nem a verdade.",
    "A dor é o megafone de Deus para despertar um mundo surdo.",
    "A coragem não é simplesmente uma das virtudes, mas a forma de toda virtude no ponto de teste.",
]


def _count_markers(text: str, markers: set) -> int:
    """Conta ocorrências de marcadores no texto."""
    text_lower = text.lower()
    count = 0
    for marker in markers:
        # Usa regex para match de palavras completas
        pattern = r'\b' + re.escape(marker) + r'\b'
        count += len(re.findall(pattern, text_lower))
    return count


def _find_markers(text: str, markers: set) -> List[str]:
    """Encontra quais marcadores estão presentes no texto."""
    text_lower = text.lower()
    found = []
    for marker in markers:
        pattern = r'\b' + re.escape(marker) + r'\b'
        if re.search(pattern, text_lower):
            found.append(marker)
    return found


def _calculate_style_similarity(text: str, corpus: List[str]) -> float:
    """
    Calcula similaridade estilística com corpus de referência.
    Usa TF-IDF + Cosine Similarity se sklearn disponível.
    """
    if not HAS_SKLEARN or not corpus:
        # Fallback: heurística simples baseada em marcadores
        analogy_count = _count_markers(text, ANALOGY_MARKERS)
        humility_count = _count_markers(text, HUMILITY_MARKERS)
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        return min((analogy_count + humility_count) / (word_count / 50), 1.0)
    
    try:
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=500,
            stop_words=None  # Manter stop words para capturar estilo
        )
        
        all_texts = corpus + [text]
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Similaridade entre texto gerado (último) e corpus
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])
        
        return float(similarities.mean())
    except Exception:
        return 0.0


def check_lewis_style(
    text: str,
    corpus: List[str] = None,
    min_similarity: float = 0.15,
    require_analogies: bool = True
) -> Dict[str, Any]:
    """
    Verifica fidelidade ao estilo C.S. Lewis.
    
    Args:
        text: Texto a ser validado
        corpus: Corpus de referência (usa padrão se None)
        min_similarity: Similaridade mínima exigida (0.0-1.0)
        require_analogies: Se True, exige pelo menos uma analogia
    
    Returns:
        Dict com style_fidelity, has_analogies, feedback
    """
    if corpus is None:
        corpus = LEWIS_REFERENCE_CORPUS
    
    feedback = []
    score = 100
    
    # 1. Detectar marcadores de analogia
    analogies_found = _find_markers(text, ANALOGY_MARKERS)
    has_analogies = len(analogies_found) > 0
    
    if require_analogies and not has_analogies:
        score -= 30
        feedback.append(
            "VIOLAÇÃO: Estilo Lewis requer analogias. "
            "Use expressões como 'imagine', 'é como se', 'suponha'."
        )
    elif has_analogies:
        feedback.append(f"OK: Analogias encontradas ({', '.join(analogies_found[:3])})")
    
    # 2. Verificar humildade intelectual
    humility_found = _find_markers(text, HUMILITY_MARKERS)
    if not humility_found:
        score -= 10
        feedback.append(
            "ALERTA: Considere adicionar marcadores de humildade "
            "('parece-me', 'suponho', 'talvez')."
        )
    
    # 3. Verificar progressão lógica
    logical_found = _find_markers(text, LOGICAL_MARKERS)
    has_logical_flow = len(logical_found) >= 2
    
    if not has_logical_flow and len(text.split()) > 100:
        score -= 10
        feedback.append(
            "ALERTA: Textos longos devem ter progressão lógica "
            "('portanto', 'primeiro... segundo')."
        )
    
    # 4. Calcular similaridade estilística
    style_similarity = _calculate_style_similarity(text, corpus)
    
    if style_similarity < min_similarity:
        score -= 20
        feedback.append(
            f"ALERTA: Baixa fidelidade estilística ({style_similarity:.1%}). "
            "O texto pode estar muito distante do tom Lewis."
        )
    
    # 5. Verificar ancoragem concreta (Lewis sempre ancora abstrações)
    abstract_without_anchor = _detect_unanchored_abstractions(text)
    if abstract_without_anchor:
        score -= 15
        feedback.append(
            f"ALERTA: Conceitos abstratos sem ancoragem: {', '.join(abstract_without_anchor[:3])}"
        )
    
    return {
        "is_compliant": score >= 70,
        "score": max(score, 0),
        "style_fidelity": round(style_similarity, 4),
        "has_analogies": has_analogies,
        "has_humility": len(humility_found) > 0,
        "has_logical_flow": has_logical_flow,
        "detected": {
            "analogies": analogies_found,
            "humility_markers": humility_found,
            "logical_markers": logical_found
        },
        "feedback": feedback if feedback else ["OK: Texto aprovado no estilo Lewis."]
    }


def _detect_unanchored_abstractions(text: str) -> List[str]:
    """
    Detecta conceitos abstratos sem ancoragem em experiência concreta.
    (Implementação simplificada - em produção usaria NLP mais sofisticado)
    """
    # Conceitos abstratos comuns que precisam de ancoragem
    abstract_concepts = {
        'moralidade', 'virtude', 'pecado', 'salvação', 'graça',
        'eternidade', 'infinito', 'absoluto', 'transcendente',
        'consciência', 'alma', 'espírito', 'livre arbítrio',
        'justiça', 'verdade', 'beleza', 'bondade'
    }
    
    text_lower = text.lower()
    words = set(re.findall(r'\b\w+\b', text_lower))
    
    found_abstract = words & abstract_concepts
    
    # Verifica se há analogias próximas (simplificado)
    has_nearby_analogy = bool(_find_markers(text, ANALOGY_MARKERS))
    
    if found_abstract and not has_nearby_analogy:
        return list(found_abstract)
    
    return []


# Exemplo de uso
if __name__ == "__main__":
    # Texto BOM (estilo Lewis)
    texto_lewis_bom = """
    O arrependimento, parece-me, não é simplesmente sentir-se mal pelo que fizemos.
    Imagine que você está a montar um puzzle e percebe que colocou uma peça errada
    há dez peças atrás. Você não pode simplesmente continuar — deve voltar e corrigir.
    Esse "voltar atrás" é o que chamamos de arrependimento. Portanto, arrependimento
    é menos sobre emoção e mais sobre correção.
    """
    
    # Texto RUIM (técnico, sem analogias)
    texto_ruim = """
    O arrependimento é definido teologicamente como a mudança de mente e coração
    que leva à conversão. É um conceito soteriológico fundamental na tradição
    cristã, envolvendo aspectos cognitivos, emocionais e volitivos.
    """
    
    print("=== Texto Estilo Lewis ===")
    r1 = check_lewis_style(texto_lewis_bom)
    print(f"Compliant: {r1['is_compliant']}, Score: {r1['score']}")
    print(f"Fidelidade: {r1['style_fidelity']:.1%}")
    print(f"Analogias: {r1['detected']['analogies']}")
    
    print("\n=== Texto Técnico ===")
    r2 = check_lewis_style(texto_ruim)
    print(f"Compliant: {r2['is_compliant']}, Score: {r2['score']}")
    print(f"Feedback: {r2['feedback']}")
