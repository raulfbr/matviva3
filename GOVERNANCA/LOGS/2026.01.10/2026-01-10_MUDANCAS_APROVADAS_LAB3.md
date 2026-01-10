# 📋 MUDANÇAS APROVADAS — Lab V3 Refinamento

**Data:** 10/Jan/2026 08:22  
**Status:** ✅ APROVADO PELO MAESTRO

---

## 1. Cards dos Guardiões (Visual-Card Style)

### Estrutura HTML Aprovada

```html
<div style="
    border-color: [COR_DO_GUARDIÃO];
    padding-top: 0;
    overflow: hidden;
    background: #fdfbf7;
    border: 2px solid [COR_DO_GUARDIÃO];
    border-radius: 12px;
    padding: 1rem;
    margin: 2rem auto;
    text-align: center;
    box-shadow: 0 8px 20px rgba([COR_RGB], 0.15);
    max-width: 200px;
">
    <img src="../../assets/img/[IMAGEM].webp" alt="[NOME]" style="
        width: 100%;
        height: auto;
        display: block;
        margin-bottom: 0.5rem;
        border-radius: 8px;
    ">
    <span style="
        font-family: 'Merriweather', serif;
        font-size: 1.1rem;
        color: #3A4A40;
        font-weight: bold;
        display: block;
    ">[NOME]</span>
    <span style="
        font-size: 0.8rem;
        color: [COR_DO_GUARDIÃO];
        text-transform: uppercase;
        letter-spacing: 1px;
    ">[SUBTÍTULO]</span>
</div>
```

### Cores dos Guardiões

| Guardião | Cor | Hex | Subtítulo |
|:---------|:----|:----|:----------|
| 🦁 Melquior | Dourado | `#B89B5E` | O Leão |
| 🦉 Noé | Verde Floresta | `#6B7A6F` | A Coruja |
| 🦊 Celeste | Laranja | `#D4784A` | A Raposa |
| 🐻 Bernardo | Marrom | `#8B6D4C` | O Urso |
| 🐦 Íris | Verde Claro | `#7AA874` | A Pardal |

### Imagens (formato WebP)

```
dist/assets/img/melquior-leao.webp
dist/assets/img/noe-coruja.webp
dist/assets/img/celeste-raposa.webp
dist/assets/img/bernardo-urso.webp
dist/assets/img/iris-passarinho-colar.webp
```

---

## 6. Bloco "Hora de Fazer" (Zona de Ritual)

### Escopo Correto

O bloco `<div class="hora-fazer">` deve envolver **TODA a zona de ritual**:

```
hora-fazer {
    — Ritual de Entrada (O Teatro da Mente) —    ← ABRE AQUI
    — A Jornada (Imersão Total) —
    — A Ideia Viva —
    — O Caminho Dourado (Mãos na Massa) —
    — Se Quiser Voar (Opcional) —
    — Momento de Conversa (Narração da Alma) —
    — Despedida & Bênção —
    — Ritual de Encerramento (O Reino Adormece) — ← FECHA AQUI
}
```

### Verificado no HTML

No arquivo `000_INICIO_GOLD.html`:
- **Abre:** Linha 104 (`<div class="hora-fazer">`)
- **Fecha:** Linha 312 (`</div>`)

### CSS do hora-fazer

```css
.hora-fazer {
    background: rgba(184, 160, 96, 0.08);
    padding: 2rem;
    border-radius: 12px;
    margin: 2rem 0;
    border-left: 3px solid var(--color-gold);
}
```

---

## 7. Zona 1 Expandida (Preparação do Portador)

### Estrutura Aprovada (Modelo: 000_INICIO_GOLD.html)

```
ZONA 1: PREPARAÇÃO (section.portador-card)
│
├── 📋 Para o Portador de Tocha (h2)
│
├── card-grid
│   ├── 🎯 Objetivo
│   └── 🎒 Materiais
│
├── zona1-bloco (verde 4%)
│   ├── 💚 Para o Pai/Mãe (Leia antes de tudo)
│   └── Protocolo de Impecabilidade
│
├── zona1-bloco (gold 4%)
│   ├── 📜 A Bancada (Mise-en-place)
│   ├── 🎯 A Ideia Viva (O Segredo)
│   └── 📦 Vivência (checklist vertical)
│       ├── ☐ 1. O Concreto
│       ├── ☐ 2. O Belo
│       ├── ☐ 3. O Elo
│       └── ☐ 4. O Sagrado
│
├── zona1-bloco (cinza-verde 4%)
│   ├── 🎧 Áudio-Script (Somente para o Pai)
│   └── blockquote: Frase do dia
│
└── dica-do-dia
    └── 💡 Dica do Dia
```

### Cores dos Blocos

| Bloco | Background | Border-left |
|:------|:-----------|:------------|
| Para o Pai/Mãe | `rgba(58, 74, 64, 0.04)` | `var(--color-green)` |
| Bancada | `rgba(184, 160, 96, 0.04)` | `var(--color-gold)` |
| Áudio-Script | `rgba(107, 122, 111, 0.04)` | `#6B7A6F` |

---

## 8. Cátedra dos Pais (Verde Floresta)

### CSS Aprovado

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

### Conteúdo

- 🧠 O Método (Singapore Math / CPA)
- 🕊️ A Mestra (Charlotte Mason)
- 🛡️ O Veredito da Graça

---

## 9. Auditoria Colapsável

### HTML Aprovado

```html
<details class="auditoria-card">
    <summary>🛡️ Auditoria da Mestra (Clique para expandir)</summary>
    <ul>
        <li>☐ <strong>Atenção:</strong> ...</li>
        <li>☐ <strong>Hábito:</strong> ...</li>
        <li>☐ <strong>Ideia Viva:</strong> ...</li>
        <li>☐ <strong>Narração:</strong> ...</li>
    </ul>
</details>
```

---

## ✅ VERIFICAÇÃO TRIPLA (10/Jan/2026 08:55)

| Item | Linha | Status |
|:-----|:------|:-------|
| Zona 1 expandida | L34-119 | ✅ |
| hora-fazer abre | L131 | ✅ |
| Ritual de Entrada | L133 | ✅ |
| Cards Guardiões (.webp) | L162+ | ✅ |
| hora-fazer fecha | L335 | ✅ |
| catedra-pais | L339-356 | ✅ |
| auditoria-card | L368-376 | ✅ |
| Navegação | L385-388 | ✅ |
| HTML fecha | L414 | ✅ |

### Veredito Final

> **IMPECÁVEL.** O modelo 000_INICIO_GOLD.html está pronto para servir de base para as demais lições.

---

## 2. Estrutura de 3 Zonas

### Template `layout_lab_v3.html`

```
┌───────────────────────────────────────┐
│ 📋 ZONA 1: Para o Portador de Tocha  │
│    🎯 Objetivo | 🎒 Materiais | 💡 Dica│
└───────────────────────────────────────┘

    <div class="zona-ritual">
    ═══════════ ZONA 2: IMERSÃO ═══════════
    │ — Ritual de Entrada —               │
    │ — A Jornada —                       │
    │ — A Ideia Viva —                    │
    │ — Caminho Dourado — (hora-fazer)    │
    │ — Se Quiser Voar —                  │
    │ — Momento de Conversa —             │
    │ — Despedida —                       │
    │ — Ritual de Encerramento —          │
    </div>

┌───────────────────────────────────────┐
│ ZONA 3: REFLEXÃO                      │
│   📖 Por que isso importa             │
│   🛡️ Auditoria (colapsável)           │
└───────────────────────────────────────┘
```

### CSS Zona Ritual (`style_lab_v3.css`)

```css
.zona-ritual {
    background: linear-gradient(180deg,
        rgba(184, 160, 96, 0.04) 0%,
        rgba(184, 160, 96, 0.08) 50%,
        rgba(184, 160, 96, 0.04) 100%);
    padding: 3rem 2rem;
    margin: 0 calc(-1 * var(--margin-content));
    border-radius: 0;
}
```

### Hora de Fazer (destaque dentro da zona)

```css
.hora-fazer {
    background: rgba(184, 160, 96, 0.08);
    padding: 2rem;
    border-radius: 12px;
    margin: 2rem 0;
    border-left: 3px solid var(--color-gold);
}
```

---

## 3. Mudanças Removidas/Simplificadas

| Mudança | Status |
|:--------|:-------|
| Card "O que você fez" | ❌ Removido (redundante) |
| H2 internos na zona ritual | → Convertidos para `scene-marker` |
| Tags `[!RITUAL]` etc. | → Removidas pelo engine |

---

## 4. Próximos Passos

1. [ ] Aplicar estrutura de cards ao `gutenberg_lab_v3.py`
2. [ ] Regenerar todas as 32 lições
3. [ ] Testar visualmente
4. [ ] Commit final

---

## 5. Arquivo de Referência

O arquivo de teste aprovado está em:
```
dist/lab_v3/sementes/000_INICIO_GOLD.html
```

**Fonte de inspiração:** https://matematica-viva.netlify.app/licoes/01-sementes/nivel-0/licao-001
