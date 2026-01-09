"""
Scriptorium Auditor
Performs a final 'Triple Verification' on produced lessons before Release.
"""
import os
import sys

# Add project root path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Scriptorium.adk.core import Session
from Scriptorium.adk.providers import GeminiProvider
from Scriptorium.agents import supervisor

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def audit_and_finalize(council, session, draft_path, output_path, lesson_name):
    print(f"\n🔍 AUDITING: {lesson_name}")
    draft_content = read_file(draft_path)
    
    # 1. Mason Audit (Tone & Vibe)
    print("   > 🏛️ Mason checking Narrative & Tone...")
    mason_check = council.mason.run(
        f"Atue como Auditora de Qualidade Charlotte Mason. Leia esta lição. O tom é 'vivo' e respeitoso? Há 'twaddle' (bobagem infantilóide)? Se estiver bom, diga APROVADO. Se não, liste correções. Lição: {draft_content[:4000]}", 
        session
    )
    
    # 2. Singapore Audit (Math Correctness)
    print("   > 📐 Singapore checking CPA Sequence...")
    singapore_check = council.singapore.run(
        f"Atue como Auditor Matemático. A etapa CONCRETA (Mãos na Massa) está clara e fisicamente viável? O conceito matemático está correto? Lição: {draft_content[:4000]}", 
        session
    )
    
    # 3. Final Polish (Headmaster)
    print("   > 🎓 Headmaster finalizing Release...")
    final_prompt = f"""
    Como Diretor do Scriptorium, você tem o rascunho Final e os pareceres da auditoria.
    
    Parecer Mason: {mason_check}
    Parecer Singapore: {singapore_check}
    
    Tarefa:
    1. Se houver críticas graves, corrija o texto no arquivo.
    2. Se estiver tudo bem, mantenha como está.
    3. RETORNE O ARQUIVO MARKDOWN COMPLETO E FINALIZADO para ser salvo na pasta de Releases.
    4. Não adicione comentários extras, apenas o conteúdo do arquivo.
    
    Arquivo Original:
    {draft_content}
    """
    
    final_content = council.provider.generate(final_prompt)
    save_file(output_path, final_content)
    print(f"   ✅ RELEASED: {output_path}")

def main():
    print("=== SCRIPTORIUM AUDIT PROCESS ===")
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    source_dir = os.path.join(base_dir, "curriculo", "_SISTEMA", "PRODUCAO")
    release_dir = os.path.join(base_dir, "Scriptorium", "RELEASES", "2026-01-09-Batch1")
    
    # Init Council
    key_path = os.path.join(base_dir, "Scriptorium", ".api_key")
    with open(key_path, 'r') as f:
        api_key = f.read().strip()
    
    provider = GeminiProvider(api_key, model_name="gemini-3-flash-preview")
    council = supervisor.Council(provider)
    session = Session()

    # Audit L000
    audit_and_finalize(
        council, session,
        os.path.join(source_dir, "000_INICIO_GOLD.md"),
        os.path.join(release_dir, "L000_O_INICIO_GOLD_FINAL.md"),
        "Lesson 000"
    )

    # Audit L001
    audit_and_finalize(
        council, session,
        os.path.join(source_dir, "001_NUMEROS_GOLD.md"),
        os.path.join(release_dir, "L001_PRIMEIROS_NUMEROS_GOLD_FINAL.md"),
        "Lesson 001"
    )

if __name__ == "__main__":
    main()
