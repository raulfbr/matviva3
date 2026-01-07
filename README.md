<p align="center">
  <img src="https://img.shields.io/badge/Vers%C3%A3o-3.5%20Sovereign%20Positive%20Gold-D4A84B?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/Licen%C3%A7a-CC%20BY%204.0-8B7355?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Pedagogia-Charlotte%20Mason-7B68B8?style=flat-square" alt="Pedagogy">
</p>

<h1 align="center">🦁 Matemática Viva</h1>

<p align="center">
  <strong>Uma jornada de 0 a 18 anos através do Reino Contado</strong><br>
  <em>"A Matemática não é uma coleção de truques abstratos — é a linguagem com a qual o Rei escreveu o Universo."</em>
</p>

---

## 👑 O Que é o Matemática Viva?

O **Matemática Viva** é um currículo de educação matemática domiciliar que transforma números frios em **Ideias Vivas**. Inspirado em **Charlotte Mason** e na pedagogia clássica, o projeto convida a criança a entrar no **Reino Contado** — um mundo onde os números falam, as formas têm nomes e a beleza matemática aponta para a Ordem do Criador.

> *"O Reino Contado não é Nárnia nem a Terra Média. É a Realidade Vista com Óculos de Maravilhar."*

### 🌿 Filosofia Central

*   **A Criança é uma Pessoa** (Princípio 1 de Charlotte Mason).
*   **Things Before Signs**: Tocamos a verdade com as mãos antes de capturá-la com símbolos (Método CPA de Singapura).
*   **Banquete de Ideias**: Apresentamos, nunca explicamos demais. O aprendizado é sempre um convite, nunca uma ordem.
*   **Zero Telas até os 10 anos** (recomendação): O digital serve ao pai, não ao filho.

---

## 🏰 O Reino Contado: Arquitetura da Jornada

O currículo acompanha o Viajante desde o berço até a maestria:

| Fase | Anos | Arquétipo | Foco Narrativo |
| :--- | :--- | :--- | :--- |
| 🌱 **Sementes** | 4-6 | Filho Herdeiro | A Realidade Saborosa. A história *é* a jornada. |
| 🌳 **Raízes** | 7-10 | Ajudante Construtor | O Contexto Vital. Matemática como ferramenta. |
| 🛡️ **Lógica** | 11-14 | Investigador Lógico | O Propósito Elevado. A clareza da razão. |
| 👑 **Legado** | 15-18 | Parceiro Mordomo | A Mordomia Real. O governo através da Ordem. |

### 🦉 Os Guardiões do Reino

Cinco personagens arquetípicos guiam o Viajante:

| Guardião | Símbolo | Virtude | Cor |
| :--- | :--- | :--- | :--- |
| **Melquior** | ☀️ Sol | Sabedoria | `#D4A84B` |
| **Noé** | 🌙 Lua | Paciência | `#7B68B8` |
| **Celeste** | ⭐ Estrela | Curiosidade | `#E8A87C` |
| **Bernardo** | 🪨 Pedra | Persistência | `#8B7355` |
| **Íris** | 🌸 Flor | Atenção | `#7EC8C8` |

---

## 🛠️ Tecnologia

O site é gerado por um motor customizado em Python (o **Gutenberg Engine**) que transforma arquivos Markdown em páginas HTML estáticas.

### Estrutura do Repositório

```
├── curriculo/          # Lições em Markdown (o coração do projeto)
├── scripts/
│   └── gutenberg.py    # Motor de geração
├── assets/             # Imagens e estilos
├── GOVERNANCA/         # Documentos de governança (O Pentateuco de Ouro)
└── dist/web/           # Site gerado (output)
```

### Rodar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/raulfbr/matematica-viva-v3.git
cd matematica-viva-v3

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Gere o site
python scripts/gutenberg.py
```

O site estará em `dist/web/`.

---

## 🚀 Deploy Automático (Vercel)

Este repositório está configurado para deploy automático no **Vercel**:

*   **Build Command:** `pip install -r requirements.txt && python scripts/gutenberg.py`
*   **Output Directory:** `dist/web`

Cada `git push` dispara uma nova build.

---

## 📜 Licenciamento

### Conteúdo Educacional

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>

Todo o conteúdo original (lições, narrativas, rituais em `curriculo/`) é disponibilizado sob a **Licença Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)**.

Você pode compartilhar e adaptar o material, desde que dê o crédito apropriado ao **Matemática Viva**.

### Código Fonte

Os scripts de geração (`scripts/`) são disponibilizados sob a licença **MIT**.

---

## 🏛️ Patronos Intelectuais

O projeto se apoia em gigantes:

*   **Charlotte Mason** — A Mestra Chefe. Filosofia e ritmo.
*   **Singapore Math** — Rigor técnico e progressão CPA.
*   **C.S. Lewis** — Afeições Ordenadas.
*   **J.R.R. Tolkien** — A Sub-criação e a Consistência Interna.
*   **Makoto Fujimura** — Culture Care e a Beleza Gratuita.

---

<p align="center">
  <em>Construído com ❤️ para o florescimento das famílias.</em><br>
  <strong>Família Rodrigues | Selo Gold+</strong>
</p>
