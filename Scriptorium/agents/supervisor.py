"""
Supervisor Agent - The Council Orchestrator
Coordinating the experts to produce a cohesive lesson.
"""

"""
Supervisor Agent - The Council Orchestrator
Coordinating the experts to produce a cohesive lesson.
"""

from Scriptorium.adk.core import Session, Agent
from Scriptorium.agents import definitions
import time
import os
import datetime

class Council:
    def __init__(self, provider):
        self.provider = provider
        self.mason = definitions.create_mason_agent(provider)
        self.singapore = definitions.create_singapore_agent(provider)
        self.lewis = definitions.create_lewis_agent(provider)
    
    def run_session(self, topic: str, session: Session) -> str:
        """
        Runs the 'Council Session' workflow.
        """
        print(f"\n[🔔 The Council is considering: '{topic}']")
        
        # 1. Charlotte Mason
        print("\n> 🏛️  Mason is speaking...")
        # time.sleep(1) 
        mason_prompt = f"Crie uma introdução narrativa curta e viva sobre: {topic}. Use o estilo narrativo, sem listas."
        mason_res = self.mason.run_with_retry(mason_prompt, session, "validate_mason_style")
        
        # 2. Singapore Math
        print("\n> 📐 Singapore is modeling...")
        time.sleep(1)
        if 'phase' not in session.state: session.state['phase'] = 'CONCRETE'
        phase = session.state['phase']
        singapore_prompt = f"Com base na narrativa sobre {topic}, explique o conceito matemático usando a abordagem {phase} (CPA)."
        singapore_res = self.singapore.run_with_retry(singapore_prompt, session, "validate_singapore_phase")
        
        # 3. C.S. Lewis
        print("\n> 🦁 Lewis is reflecting...")
        time.sleep(1)
        lewis_prompt = f"Faça uma breve reflexão analógica conectando o tema '{topic}' a uma verdade maior ou moral, no estilo de C.S. Lewis."
        lewis_res = self.lewis.run_with_retry(lewis_prompt, session, "validate_lewis_style")
        
        # 4. Synthesis
        print("\n> 🎓 Headmaster is synthesizing...")
        time.sleep(1)
        synthesis_prompt = (
            f"Você é o Diretor Pedagógico do Scriptorium. "
            f"Sua equipe gerou os seguintes materiais sobre '{topic}':\n\n"
            f"MASON: {mason_res}\n\n"
            f"SINGAPORE: {singapore_res}\n\n"
            f"LEWIS: {lewis_res}\n\n"
            f"Tarefa: Crie um 'Plano de Lição Unificado' que integre essas três visões numa aula coesa para uma criança de 6 anos. "
            f"Comece com a narrativa, siga para a atividade prática (matemática) e termine com o momento de contemplação (Lewis). "
            f"Seja caloroso e direto e use Markdown rico."
        )
        final_plan = self.provider.generate(synthesis_prompt)

        # Log to File
        self._log_to_file(topic, mason_res, singapore_res, lewis_res, final_plan)

        # Combine for display
        full_report = (
            f"--- 📜 ATA DA REUNIÃO DO CONSELHO ---\n\n"
            f"**TEMA:** {topic}\n\n"
            f"---\n\n"
            f"{final_plan}\n\n"
            f"---\n"
            f"*(Registro salvo em ATA_REUNIAO_CONSELHO.md)*"
        )
        
        session.add_message("model", full_report)
        return full_report

    def _log_to_file(self, topic, mason, singapore, lewis, synthesis):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # .. -> agents -> Scriptorium -> Root
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ATA_REUNIAO_CONSELHO.md")
        
        entry = (
            f"\n\n# 🗓️ Reunião: {topic} ({timestamp})\n\n"
            f"## 🏛️ Charlotte Mason (Narrativa)\n{mason}\n\n"
            f"## 📐 Singapore Math (Modelo)\n{singapore}\n\n"
            f"## 🦁 C.S. Lewis (Reflexão)\n{lewis}\n\n"
            f"## 🎓 SÍNTESE DO DIRETOR\n{synthesis}\n\n"
            f"---"
        )
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)

