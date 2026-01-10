# 🧠 CONTEXTO COMPLETO: LAB V3 ENGINE — RENOVAÇÃO DE LAYOUT

**Data:** 10/Jan/2026  
**Status:** ⏳ EM ANDAMENTO  
**Objetivo:** Documentar todas as decisões de layout para que uma IA futura possa continuar o trabalho.

---

## 1. VISÃO GERAL DO SISTEMA

### Arquivos Envolvidos

| Arquivo | Tipo | Descrição |
|:--------|:-----|:----------|
| `curriculo/01_SEMENTES_TESTE/*.md` | Fonte | 32 arquivos Markdown com conteúdo das lições |
| `gutenberg_lab_v3.py` | Engine | Script Python que converte MD → HTML |
| `curriculo/_SISTEMA/TEMPLATES/layout_lab_v3.html` | Template | Estrutura HTML base |
| `curriculo/_SISTEMA/TEMPLATES/style_lab_v3.css` | CSS | Estilos visuais |
| `dist/lab_v3/sementes/*.html` | Output | HTML gerado |
| `dist/lab_v3/sementes/000_INICIO_GOLD.html` | **MODELO** | HTML de referência editado manualmente |

### Fluxo de Trabalho

```
[MD Fonte] → [gutenberg_lab_v3.py] → [HTML Gerado]
                    ↓
            [layout_lab_v3.html] + [style_lab_v3.css]
```

---

## 2. ESTRUTURA DE 3 ZONAS

O layout Lab V3 é dividido em **3 zonas visuais**:

```
┌─────────────────────────────────────────────────────────────┐
│ ZONA 1: PREPARAÇÃO (section.portador-card)                  │
│   → Para o Portador de Tocha (somente pai/mãe lê)           │
│   → Card branco com conteúdo preparatório                   │
└─────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────┐
│ ZONA 2: IMERSÃO (div.zona-ritual > article.jornada-fluida)  │
│   → Background cream unificado                              │
│   → Conteúdo narrativo lido COM a criança                   │
│   │                                                         │
│   ├── <div class="hora-fazer">                              │
│   │   — Ritual de Entrada →                                 │
│   │   — A Jornada →                                         │
│   │   — Ideia Viva →                                        │
│   │   — Caminho Dourado →                                   │
│   │   — Se Quiser Voar →                                    │
│   │   — Momento de Conversa →                               │
│   │   — Despedida →                                         │
│   │   — Ritual de Encerramento                              │
│   └── </div>                                                │
│                                                             │
│   └── <div class="catedra-pais">                           │
│       🏛️ Por que isso importa? (reflexão para o pai)       │
│       </div>                                                │
└─────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────┐
│ ZONA 3: REFLEXÃO (section.reflexao-cards)                   │
│   → <details class="auditoria-card"> (colapsável)           │
│   → Checklist de verificação CM                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. ZONA 1: ESTRUTURA DETALHADA

### O que NÃO está na Zona 1 (removido)
- ❌ Cards de Objetivo e Materiais (eram redundantes)

### O que ESTÁ na Zona 1

```html
<section class="portador-card">
    <h2>📋 Para o Portador de Tocha</h2>

    <!-- Bloco 1: Para o Pai/Mãe -->
    <div class="zona1-bloco" style="background: rgba(58, 74, 64, 0.04); border-left: 3px solid var(--color-green);">
        <h3>💚 Para o Pai/Mãe (Leia antes de tudo)</h3>
        <p>[Mensagem de encorajamento]</p>
        <p><strong>Protocolo de Impecabilidade:</strong> [Instruções]</p>
    </div>

    <!-- Bloco 2: A Bancada -->
    <div class="zona1-bloco" style="background: rgba(184, 160, 96, 0.04); border-left: 3px solid var(--color-gold);">
        <h3>📜 A Bancada (Mise-en-place)</h3>
        <p><strong>A Liturgia da Ordem:</strong> [Explicação]</p>
        
        <div>
            <p>🎯 <strong>A Ideia Viva (O Segredo):</strong></p>
            <p>[Conceito central da lição]</p>
        </div>

        <div>
            <p>📦 <strong>Vivência (Exploração Sensorial):</strong></p>
            <ul>
                <li>☐ 1. O Concreto: [material físico]</li>
                <li>☐ 2. O Belo: [elemento estético]</li>
                <li>☐ 3. O Elo: [conexão emocional]</li>
                <li>☐ 4. O Sagrado: [elemento ritual]</li>
            </ul>
        </div>
    </div>

    <!-- Bloco 3: Áudio-Script -->
    <div class="zona1-bloco" style="background: rgba(107, 122, 111, 0.04); border-left: 3px solid #6B7A6F;">
        <h3>🎧 Áudio-Script (Somente para o Pai)</h3>
        <p><em>Opção A / Opção B</em></p>
        <blockquote style="background: rgba(184, 160, 96, 0.08);">
            "[Frase do dia para o pai meditar]"
        </blockquote>
    </div>

    <!-- Bloco 4: Dica do Dia -->
    <div class="dica-do-dia">
        <span class="card-icon">💡</span>
        <span class="card-label">Dica do Dia</span>
        <p>[Dica rápida]</p>
    </div>
</section>
```

### Cores dos Blocos

| Bloco | Background | Border-left |
|:------|:-----------|:------------|
| Para o Pai/Mãe | `rgba(58, 74, 64, 0.04)` | `var(--color-green)` |
| Bancada | `rgba(184, 160, 96, 0.04)` | `var(--color-gold)` |
| Áudio-Script | `rgba(107, 122, 111, 0.04)` | `#6B7A6F` |

---

## 4. ZONA 2: HORA-FAZER + CÁTEDRA

### hora-fazer (Background Gold 8%)

O `<div class="hora-fazer">` DEVE envolver **todo o conteúdo da imersão**:

```
hora-fazer ABRE → — Ritual de Entrada —
                  — A Jornada —
                  — A Ideia Viva —
                  — O Caminho Dourado —
                  — Se Quiser Voar —
                  — Momento de Conversa —
                  — Despedida —
hora-fazer FECHA → — Ritual de Encerramento —
```

### CSS hora-fazer

```css
.hora-fazer {
    background: rgba(184, 160, 96, 0.08);
    padding: 2rem;
    border-radius: 12px;
    margin: 2rem 0;
    border-left: 3px solid var(--color-gold);
}
```

### catedra-pais (Background Verde 6%)

Fica **DEPOIS** do hora-fazer, ainda dentro da Zona 2.

```html
<div class="catedra-pais">
    <h2>🏛️ Por que isso importa? (A Cátedra dos Pais)</h2>
    <p>🧠 <strong>O Método (Singapore):</strong> [Explicação pedagógica]</p>
    <p>🕊️ <strong>A Mestra (CM):</strong> [Citação Charlotte Mason]</p>
    <p>🛡️ <strong>O Veredito da Graça:</strong> [Mensagem de segurança para os pais]</p>
</div>
```

### CSS catedra-pais

```css
.catedra-pais {
    background: linear-gradient(180deg,
        rgba(58, 74, 64, 0.04) 0%,
        rgba(58, 74, 64, 0.08) 50%,
        rgba(58, 74, 64, 0.04) 100%
    );
    padding: 2rem;
    border-radius: 12px;
    margin: 2rem 0;
    border-left: 4px solid var(--color-green);
}
```

---

## 5. ZONA 3: AUDITORIA COLAPSÁVEL

```html
<section class="reflexao-cards">
    <details class="auditoria-card">
        <summary>🛡️ Auditoria da Mestra (Clique para expandir)</summary>
        <ul>
            <li>☐ <strong>Atenção:</strong> O Hábito da Atenção Plena foi estimulado?</li>
            <li>☐ <strong>Hábito:</strong> A disciplina do ritual foi mantida?</li>
            <li>☐ <strong>Ideia Viva:</strong> Houve encontro com beleza?</li>
            <li>☐ <strong>Narração:</strong> A criança agiu como narradora?</li>
        </ul>
    </details>
</section>
```

---

## 6. CARDS DOS GUARDIÕES (Visual-Card Style)

Os cards das imagens dos Guardiões usam um estilo especial:

```html
<div style="
    background: #fdfbf7;
    border: 2px solid [COR];
    border-radius: 12px;
    padding: 1rem;
    margin: 2rem auto;
    text-align: center;
    box-shadow: 0 8px 20px rgba([RGB], 0.15);
    max-width: 200px;
">
    <img src="../../assets/img/[IMAGEM].webp" alt="[NOME]" style="width: 100%; border-radius: 8px;">
    <span style="font-family: 'Merriweather'; font-size: 1.1rem; font-weight: bold;">[NOME]</span>
    <span style="font-size: 0.8rem; color: [COR]; text-transform: uppercase;">[SUBTÍTULO]</span>
</div>
```

### Cores dos Guardiões

| Guardião | Cor Hex | Subtítulo |
|:---------|:--------|:----------|
| Melquior | `#B89B5E` | O Leão |
| Noé | `#6B7A6F` | A Coruja |
| Celeste | `#D4784A` | A Raposa |
| Bernardo | `#8B6D4C` | O Urso |
| Íris | `#7AA874` | A Pardal |

### Caminho das Imagens

```
dist/assets/img/melquior-leao.webp
dist/assets/img/noe-coruja.webp
dist/assets/img/celeste-raposa.webp
dist/assets/img/bernardo-urso.webp
dist/assets/img/iris-passarinho-colar.webp
```

---

## 7. MAPEAMENTO MD → HTML

### Estrutura do Markdown Fonte

O arquivo `.md` tem seções numeradas:

| Seção MD | Vai para | Zona HTML |
|:---------|:---------|:----------|
| `[!IMPORTANT]` Para o Pai/Mãe | zona1-bloco verde | ZONA 1 |
| `## 📜 1. A Bancada` | zona1-bloco gold | ZONA 1 |
| `## 🎧 2. Áudio-Script` | zona1-bloco cinza-verde | ZONA 1 |
| `## 🕯️ 3. Ritual de Entrada` | hora-fazer (início) | ZONA 2 |
| `## 🗺️ 4. A Jornada` | hora-fazer | ZONA 2 |
| `## 💡 5. A Ideia Viva` | hora-fazer | ZONA 2 |
| `## 🧱 6. Caminho Dourado` | hora-fazer | ZONA 2 |
| `## 🦋 7. Se Quiser Voar` | hora-fazer | ZONA 2 |
| `## 🗣️ 8. Momento de Conversa` | hora-fazer | ZONA 2 |
| `## 🕊️ 9. Despedida` | hora-fazer | ZONA 2 |
| `## 🌌 10. Ritual de Encerramento` | hora-fazer (fim) | ZONA 2 |
| `## 🏛️ 11. Por que isso importa` | catedra-pais | ZONA 2 |
| `## 🛡️ 12. Auditoria da Mestra` | details.auditoria-card | ZONA 3 |

---

## 8. O QUE PRECISA SER FEITO NO ENGINE

### Modificações Necessárias no `gutenberg_lab_v3.py`

1. **Zona 1: Detecção de Seções Preparatórias**
   - Detectar `[!IMPORTANT]` e `## 📜 1. A Bancada` e `## 🎧 2. Áudio-Script`
   - Envolver em blocos `zona1-bloco` com cores apropriadas
   - Colocar ANTES do `zona-ritual`

2. **Zona 2: hora-fazer**
   - Detectar início: `## 🕯️ 3. Ritual de Entrada`
   - Detectar fim: fim de `## 🌌 10. Ritual de Encerramento`
   - Envolver tudo entre esses pontos com `<div class="hora-fazer">`

3. **Zona 2: catedra-pais**
   - Detectar `## 🏛️ 11. Por que isso importa`
   - Envolver com `<div class="catedra-pais">`

4. **Zona 3: auditoria**
   - Detectar `## 🛡️ 12. Auditoria da Mestra`
   - Mover para `<details class="auditoria-card">`

5. **Cards de Imagem**
   - Converter `![CARD: Nome](...)` para estrutura visual-card com cores
   - Usar imagens `.webp` de `../../assets/img/`

---

## 9. ARQUIVO DE REFERÊNCIA

### HTML Modelo Aprovado

```
dist/lab_v3/sementes/000_INICIO_GOLD.html
```

Este arquivo foi **editado manualmente** e representa o layout final desejado.

**Verificado em:** 10/Jan/2026 08:55  
**Total de linhas:** 401  
**Status:** ✅ IMPECÁVEL

### Estrutura de Linhas

| Item | Linha |
|:-----|:------|
| Zona 1 (section.portador-card) | L34-105 |
| zona-ritual abre | L110 |
| hora-fazer abre | L118 |
| Ritual de Entrada | L120 |
| Cards Guardiões | L146+ |
| hora-fazer fecha | L322 |
| catedra-pais | L325-343 |
| zona-ritual fecha | L349 |
| Zona 3 (reflexao-cards) | L354-364 |
| Navegação | L372-376 |
| HTML fecha | L401 |

---

## 10. PRÓXIMOS PASSOS

- [ ] Atualizar `gutenberg_lab_v3.py` para detectar seções preparatórias (1-2) e mover para Zona 1
- [ ] Atualizar engine para envolver seções 3-10 com `hora-fazer`
- [ ] Atualizar engine para envolver seção 11 com `catedra-pais`
- [ ] Atualizar engine para mover seção 12 para `details`
- [ ] Atualizar engine para converter imagens em visual-card
- [ ] Regenerar todas as 32 lições
- [ ] Testar visualmente
- [ ] Commit final

---

## 11. REFERÊNCIAS

### Documentos de Governança

- `GOVERNANCA/LOGS/2026-01-10_MUDANCAS_APROVADAS_LAB3.md`
- `GOVERNANCA/LOGS/2026-01-10_CONSELHO_CATEDRA_PAIS.md`

### Especialistas Consultados

- **Steve Schoger** (`GOVERNANCA/LOGS/ESPECIALISTA_STEVE_SCHOGER.md`)
  - Princípios: "Design is about removing things", hierarquia por tamanho, cores restritas
- **Triade Viva** (`.agent/TRIADE_VIVA.md`)
  - Conselho: Charlotte Mason (Veto), Singapore (Método), Lewis (Tao)

---

**ESTE ARQUIVO É A FONTE DE VERDADE PARA CONTINUAR O TRABALHO NO LAB V3.**
