"""
Scriptorium Output Generator
Produces Lessons 000 and 001 by refining drafts via the Council.
"""
import os
import sys

# Add project root to path (Up 3 levels: file -> tools -> Scriptorium -> Root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Scriptorium.adk.core import Session
from Scriptorium.adk.providers import GeminiProvider, OpenRouterProvider
from Scriptorium.agents import supervisor

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("=== SCRIPTORIUM PRODUCTION: LESSONS 000 & 001 ===")
    
    # Paths
    # Scriptorium/tools/produce.py -> tools -> Scriptorium -> Root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    template_path = os.path.join(base_dir, "curriculo", "_SISTEMA", "TEMPLATES", "000_TEMPLATE_SEMENTES_V3-6_GOLD.md")
    draft_000_path = os.path.join(base_dir, "curriculo", "01_SEMENTES", "000_INTRODUCAO_REINO_CONTADO.md")
    draft_001_path = os.path.join(base_dir, "curriculo", "01_SEMENTES", "001_OS_PRIMEIROS_NUMEROS.md")
    
    # Read Content
    template = read_file(template_path)
    draft_000 = read_file(draft_000_path)
    draft_001 = read_file(draft_001_path)
    
    # Init Provider (Prioritize OpenRouter)
    try:
        key_path = os.path.join(base_dir, "Scriptorium", ".openrouter_key")
        with open(key_path, 'r') as f:
            api_key = f.read().strip()
        print("✅ Using DeepSeek V3 (Standard/Stable)")
        provider = OpenRouterProvider(api_key, model_name="deepseek/deepseek-chat")
    except:
        print("⚠️ OpenRouter key not found. Fallback to Gemini.")
        key_path = os.path.join(base_dir, "Scriptorium", ".api_key")
        with open(key_path, 'r') as f:
            api_key = f.read().strip()
        provider = GeminiProvider(api_key, model_name="gemini-3-flash-preview")
        
    council = supervisor.Council(provider)
    session = Session()

    # --- JOB 1: LESSON 000 ---
    print("\n[JOB 1] Refining Lesson 000 (Introduction)...")
    print("        (Aguarde... Processamento DeepSeek V3.2 Speciale pode levar 3-5 minutos)")

    # Force Portuguese System Instruction
    sys_pt = "Você é um Especialista Pedagógico do Scriptorium. Responda ESTRITAMENTE em Português Brasileiro (PT-BR)."

    # We use explicit generate calls to ensure System Instruction is passed if possible, 
    # but the Council agents use their own sys instructions. 
    # We will modify the ADK to prepend language instruction if needed, 
    # OR simpler: We append "Responda em PT-BR" to every prompt.
    
    # 1. Supervisor reads draft and asks specialized agents for critique.
    print("> Mason reviewing narrative flow...")
    mason_critique = council.mason.run(f"Analise este rascunho sob a ótica de Charlotte Mason. O que melhorar na narrativa? Responda em PT-BR. Rascunho: {draft_000[:2000]}...", session)
    
    print("> Lewis reviewing anchoring...")
    lewis_critique = council.lewis.run(f"Analise este rascunho. A transposição teológica/filosófica está correnta? Responda em PT-BR. Rascunho: {draft_000[:2000]}...", session)

    # Define Output Directory inside Scriptorium
    output_dir = os.path.join(base_dir, "Scriptorium", "OUTPUT", "2026-01-09-DeepSeek-Speciale")
    os.makedirs(output_dir, exist_ok=True)

    print("> Generating Final Artifact (L000)...")
    final_prompt = f"""
    Atue como o Editor Chefe do Scriptorium de Alta Performance.
    Sua missão: Reescrever o arquivo da Lição 000 seguindo ESTRITAMENTE o Template Gold.
    Use sua capacidade máxima de raciocínio (Speciale) para garantir tom e profundidade.
    O TEXTO FINAL DEVE ESTAR 100% EM PORTUGUÊS (PT-BR).
    
    INPUTS:
    - Rascunho: {draft_000}
    - Crítica Mason: {mason_critique}
    - Crítica Lewis: {lewis_critique}
    - Template: {template}
    
    SAÍDA:
    Apenas o código Markdown do arquivo final.
    """
    final_000 = provider.generate(final_prompt, system_instruction=sys_pt)
    
    output_path_000 = os.path.join(output_dir, "000_INICIO_GOLD.md")
    with open(output_path_000, "w", encoding="utf-8") as f:
        f.write(final_000)
    print(f"✅ Lesson 000 Saved to {output_path_000}")
    
    print("\n------------------------------------------------")
    print("Respirando por 10 segundos antes da próxima lição...")
    import time
    time.sleep(10)

    # --- JOB 2: LESSON 001 ---
    print("\n[JOB 2] Refining Lesson 001 (Numbers)...")
    print("        (Aguarde... Processamento DeepSeek V3.2 Speciale)")
    
    prompt_001_instruction = """
    INSTRUCAO DO USUARIO:
    'Principalmente a ideia da lição 1 onde o Melquior irá apresentar cada guardião para criar uma expectativa no aluno.'
    (Nota: O rascunho da L001 foca em Celeste. Se o usuário quer que Melquior apresente TODOS novamente, ou que reforce a apresentação, faça isso na Introdução ou Ritual).
    """
    
    print("> Singapore reviewing CPA alignment...")
    singapore_critique = council.singapore.run(f"Analise a atividade matemática (seção 6) deste rascunho. Está na fase CONCRETA adequada? Responda em PT-BR. Rascunho: {draft_001[:2000]}...", session)

    print("> Generating Final Artifact (L001)...")
    final_prompt_001 = f"""
    Atue como o Editor Chefe de Alta Performance.
    Reescreva a Lição 001 seguindo o Template Gold.
    O TEXTO FINAL DEVE ESTAR 100% EM PORTUGUÊS (PT-BR).
    
    INPUTS:
    - Rascunho L001: {draft_001}
    - Instrução Extra: {prompt_001_instruction}
    - Crítica Singapore: {singapore_critique}
    - Template: {template}
    
    SAÍDA:
    Apenas o código Markdown do arquivo final.
    """
    
    final_001 = provider.generate(final_prompt_001, system_instruction=sys_pt)
    
    output_path_001 = os.path.join(output_dir, "001_NUMEROS_GOLD.md")
    with open(output_path_001, "w", encoding="utf-8") as f:
        f.write(final_001)
    print(f"✅ Lesson 001 Saved to {output_path_001}")

if __name__ == "__main__":
    main()
