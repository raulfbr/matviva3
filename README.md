# 🌿 Matemática Viva
> **Infrastrutura Educacional K-12 (0-18 anos) | Open Source (CC BY 4.0)**

> *"A matemática é a linguagem com a qual Deus escreveu o universo." — Galileu Galilei*

## 🌟 O Projeto
**Matemática Viva** não é apenas um currículo; é uma infraestrutura de ensino projetada para restaurar a visão de **Ordem, Beleza e Verdade** no ensino da matemática.

Fugindo da visão utilitarista ("aprender para passar na prova"), utilizamos uma abordagem narrativa e "viva" que conecta a criança à realidade objetiva, respeitando sua pessoa e seu tempo de desenvolvimento.

---

## 🏗️ A Engenharia Pedagógica (Kernel)
Nosso "Kernel Pedagógico" é uma tríade única, rigorosamente testada:

1.  **Charlotte Mason (A Alma):** Lições curtas, hábitos de atenção, ideias vivas e respeito à dignidade da criança.
2.  **Singapura (O Método):** Estrutura CPA (**C**oncreto → **P**ictórico → **A**bstrato). A matemática começa nas mãos, não no papel.
3.  **TGTB (A Estrutura):** *Scope & Sequence* (Escopo e Sequência) moderno e visualmente rico, adaptado para a realidade brasileira.

---

## 🗺️ Mapa do Repositório

### 1. `GOVERNANCA/` (A Constituição)
Aqui residem as regras imutáveis e a filosofia do projeto. Se você quer entender "o porquê", comece aqui.
*   **[PAINEL-ESPECIALISTAS.md](GOVERNANCA/PAINEL-ESPECIALISTAS.md):** A autoridade técnica, hierarquia de decisão e personas de consultoria.
*   **[MAGNA_CARTA.md](GOVERNANCA/01_MAGNA_CARTA.md):** Os princípios fundadores e a teologia do projeto.
*   **[MANUAL_DO_OFICIO.md](GOVERNANCA/04_MANUAL_DO_OFICIO.md):** Guia prático de execução e liturgia.

### 2. `curriculo/` (O Conteúdo)
A "carne" do projeto. Milhares de ativos educacionais organizados por ciclos de maturação.
*   **`00_VIVENCIA/` (0-3 anos):** Fundamentos sensoriais.
*   **`01_SEMENTES/` (4-6 anos):** Pré-escolar e Alfabetização Matemática.
*   **`02_RAIZES/` (7-10 anos):** O ciclo fundamental (Elementary).
*   **`_SISTEMA/`:** O motor de templates e currículos mestres.

---

### 🦁 O Motor (Gutenberg v3.6)
O projeto roda sobre um gerador de sites estático customizado (`gutenberg.py`) que:
1.  **Converte Markdown para HTML:** Preservando a semântica e acessibilidade.
2.  **Visuals Engine:** Mapeia automaticamente Guardiões e Locais para assets otimizados.
3.  **Image Optimizer:** Converte uploads brutos para WebP automaticamente.
4.  **Family Dashboard:** Gera o "Painel do Lar" para gestão de atmosfera e ritmo.

## 💻 Tech Stack & Pipeline (Vercel Ready)
Este projeto utiliza uma abordagem **"Doc-as-Code"**:
1.  **Input:** Todo o conteúdo é escrito em **Markdown** puro.
2.  **Engine (Roadmap):** Scripts Python + Jinja2 para automação de build.
3.  **Output:** Geração automática de **PDFs (Print)** e **Web App (Vercel)**.

> *Status: O repositório está estruturado para conexão futura com Vercel para deploy contínuo da versão web.*

---

## 🤝 Licença & Contribuição
Este projeto é **Open Source** sob a licença **[Creative Commons Attribution 4.0 International (CC BY 4.0)](http://creativecommons.org/licenses/by/4.0/)**.

*   **Você pode:** Compartilhar, copiar, distribuir e adaptar o material.
*   **Você deve:** Atribuir o crédito apropriado ao "Matemática Viva".

---

**[Raul Rodrigues](https://github.com/raulfbr)**
*Diretor & Maestro*
