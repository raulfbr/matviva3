# 🧑‍💻 ESPECIALISTA EXTERNO: STEVE SCHOGER

**Data de Registro:** 10/Jan/2026  
**Área:** UI/UX Design, Frontend, Minimalismo Visual  
**Status:** Especialista Ad-Hoc para consultoria de design

---

## 📋 FICHA TÉCNICA

| Campo | Valor |
|:------|:------|
| **Nome Completo** | Steve Schoger |
| **Nacionalidade** | Canadense |
| **Especialidade** | UI Design, Visual Design, Frontend |
| **Empresa** | Tailwind Labs (co-fundador) |
| **Obra Principal** | *Refactoring UI* (2018, com Adam Wathan) |
| **Twitter/X** | [@steveschoger](https://x.com/steveschoger) |
| **Website** | [steveschoger.com](https://steveschoger.com) |

---

## 🎯 FILOSOFIA DE DESIGN

### O Manifesto Schoger

> *"Design is mostly about removing things, not adding them."*  
> *"The best interface is no interface."*  
> *"If you can see the design, it's probably too much design."*

### Princípios Fundamentais

1. **Espaço em Branco é Design**
   - O vazio não é "falta de design", é uma escolha intencional
   - Padding generoso > elementos comprimidos
   - O silêncio visual prepara a atenção

2. **Hierarquia através de Tamanho, não de Estilo**
   - Use tamanho de fonte para criar hierarquia
   - Evite múltiplos estilos (negrito, itálico, sublinhado, cores diferentes) no mesmo contexto
   - Uma cor de destaque é suficiente

3. **Cores: Menos é Exponencialmente Mais**
   - Paleta restrita (3-5 cores máximo)
   - Variações de uma cor > muitas cores diferentes
   - Texto: nunca preto puro (#000), use #1a1a1a ou similar

4. **Tipografia é 90% do Design**
   - Fonte grande o suficiente para leitura confortável (18-20px mínimo)
   - Line-height de 1.5-2.0 para texto longo
   - 45-75 caracteres por linha (ideal: 65ch)

5. **Bordas e Sombras com Moderação**
   - Bordas dividem, sombras elevam
   - Use sombras sutis (blur alto, opacidade baixa)
   - Evite bordas de 1px em tudo — torna a interface "pesada"

---

## 📚 OBRA: REFACTORING UI

### Sobre o Livro

- **Título:** Refactoring UI
- **Autores:** Steve Schoger & Adam Wathan
- **Ano:** 2018
- **Formato:** E-book com exemplos visuais
- **Preço:** ~$99 USD
- **Descrição:** Guia prático para desenvolvedores que querem fazer design bonito sem ser designers formais

### Capítulos Relevantes para o Projeto

| Capítulo | Aplicação no Lab 2 |
|:---------|:-------------------|
| **Starting from Scratch** | Não comece pelo visual, comece pelo conteúdo |
| **Hierarchy is Everything** | Usar tamanho de fonte, não cores, para criar hierarquia |
| **Layout and Spacing** | Espaçamento generoso entre elementos |
| **Designing Text** | Line-height, font-size, max-width para leitura |
| **Working with Color** | Paleta restrita, uma cor de destaque |
| **Creating Depth** | Sombras sutis, evitar bordas pesadas |
| **Working with Images** | Imagens com propósito, não decoração |
| **Finishing Touches** | Micro-interações que não distraem |

---

## 🔧 APLICAÇÕES PRÁTICAS NO MATEMÁTICA VIVA

### Recomendações de Schoger para o Lab 2

#### 1. Tipografia

```css
/* ANTES (Lab 2 atual) */
--font-size-base: 1.35rem;
--line-height: 1.95;
max-width: 680px;

/* DEPOIS (Schoger-approved) */
--font-size-base: 1.4rem;   /* Ligeiramente maior */
--line-height: 2.0;         /* Mais arejado */
max-width: 75ch;            /* Baseado em caracteres, não pixels */
```

#### 2. Cores

```css
/* ANTES: Múltiplas cores de blockquote */
blockquote.ritual { border-left-color: #8B5CF6; }
blockquote.mestra { border-left-color: #EA580C; }
blockquote.narrativa { border-left-color: #3B82F6; }
blockquote.atividade { border-left-color: #22C55E; }

/* DEPOIS: Cor unificada (Gold do Reino) */
blockquote { border-left-color: #D4A84B; }
```

#### 3. Navegação

```css
/* ANTES: Pills estilo "app" */
.lab2-nav {
    background: var(--color-green);
    padding: 0.5rem 0.75rem;
    border-radius: 50px;
}

/* DEPOIS: Links texto estilo "livro" */
.lab2-nav {
    background: transparent;
    padding: 2rem 0;
    text-align: center;
    font-family: var(--font-ui);
}
.lab2-nav a {
    color: var(--color-ink-soft);
    text-decoration: none;
    padding: 0.5rem 1rem;
}
```

#### 4. Header Auto-Hide

```javascript
// Schoger recomenda header que aparece no scroll up
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const header = document.querySelector('.lab2-header');
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > lastScroll && currentScroll > 60) {
        header.style.transform = 'translateY(-100%)';
    } else {
        header.style.transform = 'translateY(0)';
    }
    lastScroll = currentScroll;
});
```

---

## 🏛️ INTEGRAÇÃO COM O PAINEL DE ESPECIALISTAS

### Onde Schoger se Encaixa

```
┌─────────────────────────────────────────────────────────────────┐
│  📚 CONSELHO PEDAGÓGICO (Charlotte Mason, Bruner, Vygotsky)    │
├─────────────────────────────────────────────────────────────────┤
│  🎨 CONSELHO DE DESIGN                                          │
│  ├── Beatrix Potter (Naturalismo Visual)                        │
│  ├── Sofia (UX Lead - Mobile-First)                             │
│  ├── Miguel (Art Director - Tipografia)                         │
│  └── ★ Steve Schoger (Minimalismo UI) ← NOVO                   │
├─────────────────────────────────────────────────────────────────┤
│  🖋️ CONSELHO NARRATIVO (Lewis, Tolkien, Fujimura)              │
├─────────────────────────────────────────────────────────────────┤
│  💼 CONSELHO DE NEGÓCIOS (Godin, Hormozi, Thiel)                │
└─────────────────────────────────────────────────────────────────┘
```

### Protocolo de Ativação

```
"Ative o Modo Schoger para auditar esta interface."

Critérios de Auditoria:
1. A paleta de cores tem mais de 5 cores? → Reduzir
2. O line-height é menor que 1.8? → Aumentar
3. Existem bordas de 1px em elementos? → Substituir por sombras ou espaço
4. O texto tem mais de 75 caracteres por linha? → Restringir max-width
5. Existem elementos decorativos que não servem ao conteúdo? → Remover
```

---

## 📖 CITAÇÕES PARA USO EM DECISÕES

> *"Don't use grey text on a grey background. That's contrast, not subtlety."*

> *"If you're using more than three font sizes, you're probably doing something wrong."*

> *"Shadows should be almost invisible. If you can see them clearly, they're too strong."*

> *"The best way to make something look designed is to give it room to breathe."*

> *"Color should be used to attract attention to important things, not to make things look pretty."*

---

## 🔗 RECURSOS ADICIONAIS

- **Livro:** [Refactoring UI](https://www.refactoringui.com/)
- **Twitter Tips:** [@steveschoger](https://x.com/steveschoger) — posts diários com dicas visuais
- **Heroicons:** [heroicons.com](https://heroicons.com/) — ícones minimalistas criados por Schoger
- **Tailwind CSS:** [tailwindcss.com](https://tailwindcss.com/) — framework CSS co-criado

---

## ✅ STATUS DE INTEGRAÇÃO

| Item | Status |
|:-----|:-------|
| Adicionado ao Conselho de Design | ✅ |
| Protocolo de Ativação definido | ✅ |
| Aplicações práticas documentadas | ✅ |
| Citações para uso em decisões | ✅ |

---

> [!NOTE]
> **Uso Recomendado:** Invocar Steve Schoger sempre que o objetivo for **simplificar** uma interface. Ele é o contraponto à tendência de "adicionar mais coisas". Seu veto é: *"Isso precisa mesmo existir?"*
