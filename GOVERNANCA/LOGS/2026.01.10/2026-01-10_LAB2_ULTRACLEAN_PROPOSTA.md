# 🧪 LAB 2 ULTRA-CLEAN: PROJETO DE REDESIGN MOBILE-FIRST

**Data:** 10/Jan/2026  
**Status:** Proposta para Deliberação  
**Autor:** Arquiteto AI + Conselho de TI Externo

---

## 🎯 OBJETIVO

Redesenhar o **Lab 2** para ser **ultra-clean** e **mobile-first**, priorizando:
1. **Legibilidade absoluta** no celular com uma mão (One-Handed Test)
2. **Zero distração visual** — apenas conteúdo
3. **Fluidez narrativa** — leitura como livro, não como app

---

## 👥 MESA DE ESPECIALISTAS CONVOCADA

### 🔵 Especialistas Internos (Governança)
| Nome | Função | Critério de Aprovação |
|:-----|:-------|:----------------------|
| **Charlotte Mason** | Pedagogia | "A criança é uma pessoa. O hábito da atenção é sagrado." |
| **Sofia (UX Lead)** | Ergonomia Mobile | "A mãe com bebê no colo consegue usar?" |
| **Beatrix Potter** | Naturalista Visual | "A beleza emerge do conteúdo, não da moldura." |

### 🟢 Especialista Externo (TI/Frontend)
| Nome | Função | Critério de Aprovação |
|:-----|:-------|:----------------------|
| **Steve Schoger** | UI/UX Minimalista | "Design é tirar coisas, não adicionar." Autor de *Refactoring UI*. |

---

## 🔬 DIAGNÓSTICO DO LAB 2 ATUAL

O Lab 2 atual já é muito melhor que o Lab 1, mas ainda pode ser **mais limpo**:

| Elemento | Status Atual | Problema Identificado | Ação Proposta |
|:---------|:-------------|:----------------------|:--------------|
| **Header Sticky** | Presente | Ocupa espaço vertical valioso | Tornar mais fino ou auto-hide no scroll |
| **Separadores ✦ ✦ ✦** | 2 separadores | Quebram a fluidez | Reduzir para 1 ou remover |
| **Navegação Pills** | Fixed no rodapé | Estilo "app", não "livro" | Botões texto simples ou swipe gesture |
| **Guardian Line** | Avatar + texto | Distrai do conteúdo | Mover para header ou rodapé |
| **Blockquotes** | Border-left colorida | Muitas cores diferentes | Unificar para uma cor sutil |

---

## 📐 PROPOSTAS DIVERGENTES (FASE 1)

### 🅰️ Proposta "Kindle Mode" (Minimalismo Radical)
**Autor:** Steve Schoger (TI Externo)

> *"O melhor design é invisível. Se você vê o design, ele falhou."*

**Especificação:**
- **Zero header fixo** — título aparece apenas no scroll up
- **Zero navegação visível** — swipe para avançar/voltar
- **Zero ornamentos** — sem separadores, sem ícones, sem cores
- **Fonte única** — apenas Merriweather, 18px/1.8
- **Fundo:** Off-white puro (#FEFEFE)

**Prós:**
- Imersão total — parece um livro físico
- Zero distração — toda atenção no conteúdo

**Contras:**
- Curva de aprendizado (swipe não é óbvio)
- Perde a identidade visual do projeto

---

### 🅱️ Proposta "Caderno Naturalista" (Minimalismo Orgânico)
**Autor:** Sofia (UX Lead) + Beatrix Potter

> *"A beleza deve emergir do conteúdo, não da moldura. Mas o caderno tem capa."*

**Especificação:**
- **Header ultra-fino** — apenas "← Reino" e tempo (12px)
- **Título centralizado** — uma vez, no topo, com subtítulo
- **Sem separadores de ritual** — usar espaço em branco generoso
- **Blockquotes unificados** — apenas uma cor (verde floresta sutil)
- **Navegação texto** — "← Voltar | Próxima →" no rodapé, sem pills

**Prós:**
- Mantém identidade (cores do Reino)
- Navegação clara e intuitiva

**Contras:**
- Ainda tem "interface" visível

---

### 🅲️ Proposta "Scroll Infinito" (Híbrido)
**Autor:** Arquiteto AI

> *"E se a lição não tivesse fim nem início visíveis? Apenas fluxo."*

**Especificação:**
- **Header aparece/desaparece** — fade on scroll up
- **Guardian inline** — pequeno avatar ao lado do primeiro parágrafo
- **Separadores ultra-sutis** — linha de 1px a 30% de opacidade
- **Navegação flutuante** — botão circular discreto no canto

**Prós:**
- Moderno e elegante
- Flexível para diferentes tipos de conteúdo

**Contras:**
- Mais complexo de implementar
- Pode parecer "app" demais

---

## 🧭 ANÁLISE COMPARATIVA (FASE 2)

| Critério | 🅰️ Kindle | 🅱️ Caderno | 🅲️ Híbrido |
|:---------|:----------|:-----------|:-----------|
| **CM: Dignidade da Pessoa** | ✅ Foco total | ✅ Foco com guia | ⚠️ Elementos podem distrair |
| **Sofia: One-Handed Test** | ⚠️ Swipe confuso | ✅ Links claros | ✅ OK |
| **Beatrix: Beleza Orgânica** | ⚠️ Muito frio | ✅ Equilibrado | ⚠️ Pode parecer digital |
| **Steve: Minimalismo** | ✅ Perfeito | ⚠️ Ainda tem UI | ⚠️ Compromisso |
| **Teste Renata/Priscila** | ❌ Confuso | ✅ Intuitivo | ⚠️ Precisa orientação |

**Recomendação do Conselho:** Proposta **🅱️ Caderno Naturalista**

---

## 💡 SUGESTÕES DO ESPECIALISTA EXTERNO (Steve Schoger)

> *Baseado em "Refactoring UI" e princípios de design minimalista.*

### 1. Tipografia é Tudo
- Aumente para **19-20px** no mobile (17px é muito pequeno)
- Use `font-weight: 400` para corpo, `700` apenas para títulos
- Line-height de **1.9 a 2.0** para leitura confortável

### 2. Espaço em Branco é Design
- Padding lateral mínimo de **20px** (não 16px)
- Margem entre parágrafos de **2rem** (não 1.8rem)
- Antes de títulos: **4rem**, depois: **1.5rem**

### 3. Cores: Menos é Mais
- **Uma cor de destaque** (o Gold #D4A84B)
- **Texto:** #2E2A26 (não preto puro #000)
- **Fundo:** #FAF8F5 (não branco puro #FFF)
- **Blockquotes:** Todos com border-left #D4A84B (unificado)

### 4. Navegação Invisível
- **Swipe horizontal** para avançar/voltar (opcional)
- **Links texto** no rodapé (não botões)
- **No pills, no floating buttons**

---

## ❓ PERGUNTAS + RECOMENDAÇÕES DO CONSELHO

### 1. Cores dos Blockquotes (Identidade vs. Limpeza)

| Opção | Descrição |
|:------|:----------|
| **A)** | Manter cores por Guardião (Lab 2 atual: roxo ritual, laranja mestra, azul narrativa, verde atividade) |
| **B)** | Unificar em **Gold (#D4A84B)** — todos os blockquotes iguais |
| **C)** | Usar **verde floresta** sutil para todos (mais discreto que gold) |

> **🏆 Recomendação:** Opção **B (Gold unificado)**  
> *Razão:* Steve Schoger ensina que **reduzir variação de cor aumenta elegância**. O Gold já é a cor do Reino e de Melquior. Unificar cria harmonia visual sem perder identidade.

---

### 2. Navegação (Pills vs. Texto)

| Opção | Descrição |
|:------|:----------|
| **A)** | Pills coloridas (Lab 2 atual: fundo verde, pill gold) |
| **B)** | Links texto simples no rodapé ("← Voltar | Próxima →") |
| **C)** | Setas discretas nas laterais (como leitor Kindle) |

> **🏆 Recomendação:** Opção **B (Links texto)**  
> *Razão:* Pills parecem "app". Links texto parecem "livro". Alinha com o objetivo de **imersão de leitura**. Sofia (UX) aprova: menos ruído visual.

---

### 3. Header (Fixo vs. Auto-Hide)

| Opção | Descrição |
|:------|:----------|
| **A)** | Header fixo fino (altura 40px, sempre visível) |
| **B)** | Header aparece só no scroll up (desaparece ao rolar para baixo) |
| **C)** | Sem header fixo — apenas título no topo do documento |

> **🏆 Recomendação:** Opção **B (Auto-Hide)**  
> *Razão:* Maximiza área de leitura. O scroll up para ver o header é intuitivo (padrão mobile moderno). Beatrix aprova: "o contexto aparece quando a criança precisa, não quando a tela impõe".

---

### 4. Separadores de Ritual (✦ ✦ ✦)

| Opção | Descrição |
|:------|:----------|
| **A)** | Manter ornamento ✦ ✦ ✦ (Lab 2 atual) |
| **B)** | Substituir por **espaço em branco generoso** (4rem antes/depois do conteúdo) |
| **C)** | Usar **linha horizontal sutil** (1px, 30% opacidade, 50% largura) |
| **D)** | Remover completamente — fluxo contínuo |

> **🏆 Recomendação:** Opção **B (Espaço em branco)**  
> *Razão:* Charlotte Mason ensina que **o silêncio prepara a atenção**. O espaço em branco é o "silêncio visual". É mais clean que ornamentos e mais intencional que linha. Lewis aprova: "o que não se vê prepara o que se verá".

---

### 5. Implementação (Lab 3 vs. Iterar Lab 2)

| Opção | Descrição |
|:------|:----------|
| **A)** | Iterar sobre Lab 2 (modificar `style_lab_v2.css`) |
| **B)** | Criar Lab 3 do zero (novos arquivos `style_lab_v3.css`, `layout_lab_v3.html`, `gutenberg_lab_v3.py`) |

> **🏆 Recomendação:** Opção **A (Iterar Lab 2)**  
> *Razão:* O Lab 2 já tem a estrutura correta. Criar Lab 3 adiciona complexidade desnecessária. **Protocolo Exponencial:** "não criar, densificar".

---

### 6. Tamanho da Fonte Base (NOVA)

| Opção | Descrição |
|:------|:----------|
| **A)** | Manter 1.35rem (~21.6px) |
| **B)** | Aumentar para **1.4rem (~22.4px)** — mais confortável |
| **C)** | Aumentar para **1.5rem (~24px)** — grande, para quem tem dificuldade visual |

> **🏆 Recomendação:** Opção **B (1.4rem)**  
> *Razão:* Schoger recomenda 18-20px como mínimo. 1.4rem é um meio-termo entre legibilidade e economia de scroll.

---

### 7. Line-Height (Espaçamento entre Linhas) (NOVA)

| Opção | Descrição |
|:------|:----------|
| **A)** | Manter 1.95 |
| **B)** | Aumentar para **2.0** — mais arejado |
| **C)** | Aumentar para **2.1** — ultra-arejado |

> **🏆 Recomendação:** Opção **B (2.0)**  
> *Razão:* Equilibra conforto de leitura com eficiência de scroll. Estudos de UX mostram que line-height de 1.9-2.1 é ideal para leitura longa.

---

### 8. Imagem do Guardião (NOVA)

| Opção | Descrição |
|:------|:----------|
| **A)** | Manter avatar circular no título (Lab 2 atual) |
| **B)** | Mover para o **header** (ao lado do link "Reino") |
| **C)** | Remover completamente — apenas texto "Guiado por Melquior" |
| **D)** | Usar como **ícone pequeno (24px)** inline no texto |

> **🏆 Recomendação:** Opção **C (Remover)**  
> *Razão:* O avatar é bonito, mas distrai. Se o objetivo é **leitura imersiva**, o guardião deve ser sentido nas palavras, não visto na interface. Beatrix: "o ilustrador invisível é o melhor ilustrador".

---

### 9. Cor de Fundo (NOVA)

| Opção | Descrição |
|:------|:----------|
| **A)** | Manter #FAF7F2 (cream atual) |
| **B)** | Usar #FEFDFB (paper — mais claro) |
| **C)** | Usar #F5F3EE (um tom mais "pergaminho velho") |

> **🏆 Recomendação:** Opção **A (Manter #FAF7F2)**  
> *Razão:* Já está calibrado. Mudar cor de fundo é mudança sutil que pode criar inconsistência com o resto do projeto.

---

### 10. Responsividade para Desktop (NOVA)

| Opção | Descrição |
|:------|:----------|
| **A)** | Manter max-width 680px (Lab 2 atual) |
| **B)** | Aumentar para **720px** — mais espaço para tablets |
| **C)** | Usar **ch units** (ex: max-width: 75ch) — baseado em caracteres |

> **🏆 Recomendação:** Opção **C (75ch)**  
> *Razão:* Schoger e Butterick (*Practical Typography*) recomendam 45-75 caracteres por linha. Usar `ch` garante que isso seja respeitado independente da fonte.

---

## 🎯 RESUMO DAS RECOMENDAÇÕES

| # | Decisão | Recomendação |
|:--|:--------|:-------------|
| 1 | Cores Blockquotes | **Gold unificado** |
| 2 | Navegação | **Links texto** |
| 3 | Header | **Auto-Hide** |
| 4 | Separadores | **Espaço em branco** |
| 5 | Implementação | **Iterar Lab 2** |
| 6 | Fonte Base | **1.4rem** |
| 7 | Line-Height | **2.0** |
| 8 | Guardião Avatar | **Remover** |
| 9 | Cor de Fundo | **Manter** |
| 10 | Max-Width | **75ch** |

---

## 📋 PRÓXIMOS PASSOS (Após Aprovação)

1. **Mesa Rápida:** Maestro confirma ou ajusta as recomendações
2. **Editar CSS:** Modificar `style_lab_v2.css` e `layout_lab_v2.html`
3. **Rebuild:** Executar `gutenberg_lab_v2.py`
4. **Testar no Mobile:** Verificar em viewport 375px
5. **Commit:** Push para GitHub

---

## 📚 REFERÊNCIAS

- **Steve Schoger & Adam Wathan:** *Refactoring UI* (2018)
- **Charlotte Mason:** *Home Education, Vol 1* — "Short lessons, earnest and bright"
- **Governança MatViva:** `PAINEL-ESPECIALISTAS.md` — Seção 12 (UX Família)

---

> [!IMPORTANT]
> **Aguardando Deliberação do Maestro.**  
> Este documento foi criado para facilitar uma decisão informada.  
> Nenhuma alteração será feita até aprovação explícita.
