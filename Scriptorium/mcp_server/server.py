"""
Servidor MCP - Validação Pedagógica Matemática Viva

Expõe os validadores pedagógicos como ferramentas MCP que podem ser
chamadas por agentes ADK ou outras aplicações.

Uso:
    python server.py
    
    # Ou com modo debug:
    python server.py --debug
"""

import sys
import argparse
from typing import Dict, Any, Literal

# Tentativa de importar MCP
try:
    from mcp.server.fastmcp import FastMCP
    HAS_MCP = True
except ImportError:
    HAS_MCP = False
    print("AVISO: Biblioteca MCP não instalada. Rode: pip install mcp")

# Configurar path para importar validadores
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PARENT_DIR)

# Importar validadores
from validators.charlotte_mason import validate_living_style
from validators.singapore_cpa import validate_cpa_compliance
from validators.cs_lewis import check_lewis_style


# ============================================================
# CONFIGURAÇÃO DO SERVIDOR MCP
# ============================================================

if HAS_MCP:
    mcp = FastMCP(
        name="MatematicaViva-Pedagogia",
        description="Validadores pedagógicos para Matemática Viva"
    )

    @mcp.tool()
    def validate_charlotte_mason(text: str) -> Dict[str, Any]:
        """
        Valida se texto segue princípios de 'Livros Vivos' de Charlotte Mason.
        
        Verifica:
        - Ausência de bullet points/listas
        - Complexidade textual adequada (não "twaddle")
        - Densidade narrativa (pronomes, verbos de ação)
        - Diversidade lexical
        
        Args:
            text: Texto a ser validado (lição, resposta de agente, etc.)
        
        Returns:
            {is_compliant: bool, score: int, metrics: dict, feedback: list}
        """
        return validate_living_style(text)


    @mcp.tool()
    def validate_singapore_cpa(
        text: str,
        phase: Literal["CONCRETE", "PICTORIAL", "ABSTRACT"]
    ) -> Dict[str, Any]:
        """
        Valida conformidade com fase CPA (Concreto-Pictórico-Abstrato) de Singapura.
        
        Regras por fase:
        - CONCRETE: Proibido dígitos e símbolos matemáticos
        - PICTORIAL: Requer termos visuais (barra, modelo, diagrama)
        - ABSTRACT: Permite notação matemática completa
        
        Args:
            text: Texto a ser validado
            phase: Fase atual ("CONCRETE", "PICTORIAL", "ABSTRACT")
        
        Returns:
            {is_compliant: bool, score: int, violations: list, detected: dict}
        """
        return validate_cpa_compliance(text, phase)


    @mcp.tool()
    def validate_lewis_style(text: str) -> Dict[str, Any]:
        """
        Verifica fidelidade ao estilo C.S. Lewis (analogia e transposição).
        
        Verifica:
        - Presença de analogias e metáforas
        - Marcadores de humildade intelectual
        - Progressão lógica de argumentos
        - Ancoragem de abstrações em experiências concretas
        
        Args:
            text: Texto a ser validado (diálogo de Guardião, explicação, etc.)
        
        Returns:
            {is_compliant: bool, style_fidelity: float, has_analogies: bool, feedback: list}
        """
        return check_lewis_style(text)


    @mcp.tool()
    def full_pedagogical_audit(
        text: str,
        context: str = "lesson"
    ) -> Dict[str, Any]:
        """
        Auditoria pedagógica completa aplicando validadores relevantes.
        
        Args:
            text: Texto a ser auditado
            context: Tipo de conteúdo ("lesson", "math_exercise", "guardian_dialogue")
        
        Returns:
            Relatório consolidado de todos os validadores aplicáveis
        """
        results = {
            "context": context,
            "overall_compliant": True,
            "overall_score": 100,
            "validators_applied": []
        }
        
        # Charlotte Mason sempre aplica para lições
        if context in ["lesson", "guardian_dialogue"]:
            mason_result = validate_living_style(text)
            results["charlotte_mason"] = mason_result
            results["validators_applied"].append("charlotte_mason")
            if not mason_result["is_compliant"]:
                results["overall_compliant"] = False
            results["overall_score"] = min(results["overall_score"], mason_result["score"])
        
        # Lewis aplica para diálogos
        if context == "guardian_dialogue":
            lewis_result = check_lewis_style(text)
            results["cs_lewis"] = lewis_result
            results["validators_applied"].append("cs_lewis")
            if not lewis_result["is_compliant"]:
                results["overall_compliant"] = False
            results["overall_score"] = min(results["overall_score"], lewis_result["score"])
        
        # CPA aplicaria se tivéssemos a fase (não no audit geral)
        if context == "math_exercise":
            # Assume fase CONCRETE por padrão se não especificada
            cpa_result = validate_cpa_compliance(text, "CONCRETE")
            results["singapore_cpa"] = cpa_result
            results["validators_applied"].append("singapore_cpa")
            if not cpa_result["is_compliant"]:
                results["overall_compliant"] = False
            results["overall_score"] = min(results["overall_score"], cpa_result["score"])
        
        return results


# ============================================================
# MODO STANDALONE (SEM MCP)
# ============================================================

def run_standalone_test():
    """Executa testes dos validadores sem servidor MCP."""
    print("=" * 60)
    print("TESTE STANDALONE DOS VALIDADORES")
    print("=" * 60)
    
    # Teste Charlotte Mason
    print("\n📚 Charlotte Mason - Livros Vivos")
    print("-" * 40)
    
    texto_narrativo = """
    Era uma vez um menino chamado Tomás que adorava as estrelas.
    Toda noite, ele subia no telhado e contava as constelações.
    Sua avó dizia que cada estrela era uma história esperando ser contada.
    """
    
    result = validate_living_style(texto_narrativo)
    print(f"Score: {result['score']}/100")
    print(f"Aprovado: {'✅' if result['is_compliant'] else '❌'}")
    print(f"Métricas: {result['metrics']}")
    
    # Teste CPA
    print("\n🔢 Singapura CPA - Fase Concreta")
    print("-" * 40)
    
    texto_concreto = """
    Imagine que você tem três maçãs na mão esquerda.
    Agora pegue mais duas maçãs com a outra mão.
    Junte todas as maçãs. Quantas você está segurando?
    """
    
    result = validate_cpa_compliance(texto_concreto, "CONCRETE")
    print(f"Score: {result['score']}/100")
    print(f"Aprovado: {'✅' if result['is_compliant'] else '❌'}")
    print(f"Objetos concretos: {result['detected']['concrete_nouns']}")
    
    # Teste Lewis
    print("\n✨ C.S. Lewis - Estilo Analógico")
    print("-" * 40)
    
    texto_lewis = """
    A paciência, parece-me, é como cultivar um jardim.
    Não adianta puxar as plantas para que cresçam mais rápido.
    Imagine tentar fazer isso — você arrancaria as raízes! 
    Portanto, a sabedoria é regar e esperar.
    """
    
    result = check_lewis_style(texto_lewis)
    print(f"Score: {result['score']}/100")
    print(f"Aprovado: {'✅' if result['is_compliant'] else '❌'}")
    print(f"Analogias: {result['detected']['analogies']}")
    
    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Servidor MCP de Validação Pedagógica")
    parser.add_argument("--debug", action="store_true", help="Modo debug")
    parser.add_argument("--test", action="store_true", help="Rodar testes standalone")
    args = parser.parse_args()
    
    if args.test:
        run_standalone_test()
        return
    
    if not HAS_MCP:
        print("❌ MCP não está instalado. Rode os testes standalone com --test")
        print("   Ou instale MCP: pip install mcp")
        run_standalone_test()
        return
    
    print("🚀 Iniciando servidor MCP...")
    print("   Nome: MatematicaViva-Pedagogia")
    print("   Ferramentas: validate_charlotte_mason, validate_singapore_cpa,")
    print("                validate_lewis_style, full_pedagogical_audit")
    
    mcp.run()


if __name__ == "__main__":
    main()
