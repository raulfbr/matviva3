# 📋 LOG DE DISCUSSÃO: ESTRATÉGIA DE MIGRAÇÃO CANÔNICA (SEMENTES V3.6)
**Data:** 2026-01-09
**Status:** Em Discussão (Aguardando Maestro)
**Referência:** `PAINEL-ESPECIALISTAS.md` + `TRIADE_VIVA.md`

## 1. 🔍 CONTEXTO TÉCNICO (O "SISTEMA")

Atualmente, o nosso sistema de build (`gutenberg.py`) opera sobre a pasta `curriculo/01_SEMENTES`. 
- **O Desafio:** As lições em `curriculo/01_SEMENTES-UTILIZAR` são a nova "Soberania" (V3.6 Gold), mas migrá-las de uma vez pode causar entropia no build do Vercel.
- **A Oportunidade:** Testar as lições `000`, `001` e `002` como "Ponta de Lança" para validar o novo template Gold no compilador.

---

## 🏛️ 2. PARECER DO PAINEL DE ESPECIALISTAS

### 🧠 O MÉTODO (Singapore/Heurística)
O especialista de Singapura observa que o novo template Gold em `01_SEMENTES-UTILIZAR` possui uma densidade pedagógica superior (CPA mais claro). 
> "A migração deve garantir que os metadados `tgtb` e `id` sejam preservados para não quebrar a indexação do `gutenberg.py`."

### 🕊️ A MESTRA (Charlotte Mason)
A Mestra aprova a transição para o "Salto de Luz" e o vocabulário de "Portador" e "Viajante".
> "A dignidade da criança exige que o material digital seja tão belo quanto o impresso. O build deve refletir a paz da 'Bancada' (Mise-en-place)."

### 💻 O ARQUITETO (IA/Engine)
O Arquiteto alerta que o `gutenberg.py` faz substituições de strings específicas (ex: regex para limpar HUB Footer). Precisamos garantir que o novo template Gold não tenha tags que confundam o Regex atual.

---

## 🚀 3. PROPOSTA DE WORKFLOW PARA TESTE (L000 - L002)

Para não "agir" sem sua ordem, desenhei este caminho seguro:

1.  **Criação de Sandbox:** Criaríamos `curriculo/01_SEMENTES_TESTE`.
2.  **Injeção Gold:** Copiaríamos apenas `000`, `001` e `002` de `01_SEMENTES-UTILIZAR` para a pasta de teste.
3.  **Desvio do Compilador:** Alteraríamos temporariamente o `gutenberg.py` para ler de `01_SEMENTES_TESTE` em vez da pasta antiga.
4.  **Simulação de Vercel:** Rodaríamos o build local e verificaríamos se o `index.html` (portal) e as lições mantêm a "Impecabilidade" visual e funcional.

---

## ❓ 4. PERGUNTAS PARA O MAESTRO (Ajuste de Mira)

Para que eu seja **detalhista** como solicitado, preciso destas definições:

1.  **Preservação Sensível:** As lições atuais em `01_SEMENTES` possuem algum conteúdo (como links de imagens específicos ou ajustes manuais) que você teme perder, ou as de `UTILIZAR` são 100% superiores e podem substituir as antigas após o teste?
2.  **Metadados do Index:** O `gutenberg.py` usa o nome do arquivo e o `id` para gerar o Grid de Cards. Podemos renomear os arquivos da pasta `UTILIZAR` para o padrão numérico estrito (ex: `000_INTRO.md`) para garantir a ordem correta no Vercel?
3.  **A "Triade Viva" no Build:** Você deseja que eu gere uma **ATA DE REUNIÃO** (conforme `TRIADE_VIVA.md`) para cada lição migrada, ou apenas para o processo de migração do sistema?

---

**Aguardando seu sinal verde ou novas instruções no LOG.**
*O Reino adere à ordem para que a beleza floresça.*
