---
id: MESA_PIPELINE_DEPLOY
titulo: "Mesa Redonda: Engenharia do Gutenberg & Deploy"
data: 2026-01-08
hora: 16:35
presidente: Arquiteto (Dev/Ops)
especialistas: [Maestro (Estratégia), Matriarca (UX), Rainha de Copas (Crítica), Arquiteto (Tech)]
tema: "Como transformar Markdown em Site e publicar antes do jantar?"
status: Em progresso
---

# 🏗️ MESA DE ENGENHARIA: O PROTOCOLO GUTENBERG

> **Cenário:** Temos ouro em texto (`.md`), mas o mundo (Vercel) só fala HTML. O Maestro tem pressa.

---

## 🔔 FASE 1: DESENHO DA ARQUITETURA

### 1. Arquiteto (Tech) - A Proposta "Static First"
> "Senhores, Vercel é ótimo, mas configurar Python Runtime lá agora é pedir para ter dor de cabeça com *timeouts* e dependências.
> **Minha Proposta Inevitável:**
> 1.  Criamos um script local `build.py` (O Motor Gutenberg).
> 2.  Ele lê os Markdowns V3.6.
> 3.  Ele cospe HTML estático puro na pasta `/dist`.
> 4.  O GitHub empurra `/dist` para a Vercel.
>
> **Por que?** HTML estático não quebra. É rápido, é seguro, e roda em qualquer lugar (até num pendrive)."

### 2. Rainha de Copas (Crítica) - E o Legado?
> "Temos dezenas de lições velhas (V1, V2). Se o script tentar ler aquele caos, ele vai explodir.
> Vocês vão parar o mundo para refatorar 50 arquivos? Não temos tempo."

### 3. Maestro (Estratégia) - O Contrato de Escopo
> "A Rainha tem razão. Não vamos refatorar o passado agora.
> **Decisão:** O Motor Gutenberg só processará lições com `status: Canônico` e versão `3.6`.
> O resto fica na pasta `_arquivo` ou ignorado. Focamos em publicar **L000 a L004** perfeitas. É melhor um site pequeno e brilhante do que um monstro quebrado."

---

## 🎨 FASE 2: UX DO "INDEX" (A CAPA DO LIVRO)

### 1. Matriarca (UX)
> "Não quero uma lista de arquivos feia (`index of /`).
> Quero uma **Árvore da Vida**.
> O `index.html` deve mostrar:
> *   **Fase Sementes:** As lições ativas coloridas.
> *   **Lore:** Quem são os Guardiões.
> *   **Visual:** Tem que ser lindo no celular da mãe."

### 2. Arquiteto (Tech)
> "Posso usar um template Jinja2 simples.
> O `build.py` vai varrer as pastas, ler o YAML header (`titulo`, `meta`, `guardia`) e montar o Index automaticamente. Se você mudar o título no Markdown, o site atualiza sozinho."

---

## 🚀 FASE 3: PLANO DE ATAQUE (Imediato)

**O Script `gutenberg.py` deve fazer:**
1.  **Limpeza:** Apagar `/dist` antigo.
2.  **Compilação:** Converter MD -> HTML usando `markdown2` e um template HTML base (com CSS do Reino).
3.  **Indexação:** Gerar `index.html` com os cards das lições.
4.  **Assets:** Copiar imagens de `/assets` para `/dist/assets`.

**Ação no Vercel:**
*   Configurar Root Directory para `dist` (ou apenas garantir que o repo tenha o `index.html` na raiz após o build local).
*   *Correction:* Se rodarmos o build localmente e dermos push no `/dist`, sujamos o git.
*   *Melhor:* O Maestro roda `python build.py` antes de commitar. O repo contém o site pronto. O Vercel só serve. (Isso é o mais robusto para hoje).

---

## ⚔️ VEREDITO DA MESA

1.  **Motor:** Python Local (`gutenberg.py`).
2.  **Alvo:** Apenas Lições V3.6 (Sementes L000-L004). Legado ignorado por enquanto.
3.  **Index:** Gerado dinamicamente pelo script.
4.  **Deploy:** Build Local -> Push HTML -> Vercel Serve.

***Maestro, autoriza a forja do `gutenberg.py`?***
