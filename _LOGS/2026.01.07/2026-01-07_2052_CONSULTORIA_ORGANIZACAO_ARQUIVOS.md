# 🕯️ REUNIÃO DE CONSULTORIA: Organização de Arquivos

**Data:** 2026-01-07_2052
**Convocados:** DevOps, Design, Negócios, Pedagogia, Propósito
**Objetivo:** Análise profunda da estrutura de pastas e arquivos do projeto.

---

## 🏗️ 1. INVENTÁRIO ATUAL

### Pasta Raiz do Projeto (8 pastas):
| Pasta | Propósito | Filhos |
|-------|-----------|--------|
| `.agent/` | Configuração do agente IA | 1 |
| `.git/` | Controle de versão | - |
| `Arrumar/` | ⚠️ **Pasta temporária?** | 36 |
| `GOVERNANCA/` | Documentos de governança | 7 |
| `_ARQUIVO/` | Arquivos históricos/backup | 10 |
| `_Assistente_Pessoal/` | ⚠️ **Fora do escopo do projeto?** | 58 |
| `_LOGS/` | Logs de sessões | 15 |
| `curriculo/` | Conteúdo pedagógico (lições) | 141 |

---

## 🗣️ 2. DEBATE DA MESA COMPLETA

### 💻 DevOps (Engenharia):
> **Análise:**
> 1. **Estrutura Geral:** Está boa. Separação clara entre `GOVERNANCA/` (regras), `curriculo/` (conteúdo) e `_LOGS/` (rastreabilidade).
> 2. **Problema 1: `Arrumar/`:** Nome vago. Parece pasta temporária. **Decisão:** Verificar conteúdo e integrar ou arquivar.
> 3. **Problema 2: `_Assistente_Pessoal/`:** 58 arquivos. Parece fora do escopo do Matemática Viva. **Decisão:** Confirmar com Maestro se deve ficar aqui.
> 4. **Best Practice (Pesquisa Externa):** Monorepos bem estruturados usam:
>    - `docs/` para documentação transversal (nossa `GOVERNANCA/`)
>    - README.md em cada pasta importante (falta em algumas)
>    - Convenção de nomes consistente (estamos OK com prefixos numéricos)
>
> **Recomendação DevOps:**
> - Renomear `Arrumar/` para algo descritivo ou mover para `_ARQUIVO/`.
> - Adicionar README.md em `curriculo/` e subpastas.
> - Confirmar escopo de `_Assistente_Pessoal/`.

---

### 🎨 Design (Informação):
> **Análise:**
> 1. **Hierarquia Visual:** Os prefixos numéricos em `GOVERNANCA/` (00_, 01_, 02_, etc.) são excelentes para ordenação.
> 2. **Inconsistência:** `PAINEL-ESPECIALISTAS.md` e `WORKFLOW_DEIXE_EXPONENCIAL.md` não têm prefixo numérico.
>
> **Recomendação Design:**
> - Adicionar prefixos aos arquivos sem número:
>   - `PAINEL-ESPECIALISTAS.md` → `05_PAINEL_ESPECIALISTAS.md`
>   - `WORKFLOW_DEIXE_EXPONENCIAL.md` → `06_WORKFLOW_DEIXE_EXPONENCIAL.md`
> - Isso garante ordem lógica ao listar arquivos.

---

### 💼 Negócios (Estratégia):
> **Análise:**
> 1. **Acessibilidade do Preço:** O preço agora está no Painel de Especialistas (Seção Negócios). ✅ Correto.
> 2. **Risco de Navegação:** Se alguém abrir o HUB e não encontrar o preço rapidamente, pode ser fricção.
>
> **Recomendação Negócios:**
> - Manter a referência no HUB com link direto. ✅ Já feito.
> - Considerar criar um arquivo `PRICING.md` separado se o modelo ficar mais complexo no futuro.

---

### 🎓 Pedagogia (CM):
> **Análise:**
> 1. **Estrutura do Currículo:** `curriculo/` está bem organizado por ciclo (00_VIVENCIA, 01_SEMENTES, 02_RAIZES, etc.).
> 2. **Falta de Guia:** Não há README.md explicando a estrutura do currículo.
>
> **Recomendação Pedagogia:**
> - Adicionar `curriculo/README.md` explicando:
>   - Como navegar pelos ciclos
>   - O que é `_SISTEMA/`
>   - Como usar os `CURRICULOS_MESTRE`

---

### 🧭 Propósito (Metafísico):
> **Análise:**
> 1. **Coerência com North Star:** A estrutura atual reflete a missão (Saber Aberto + Experiência Premium)?
> 2. **Resposta:** Sim. `curriculo/` contém o "Saber Aberto". `GOVERNANCA/` contém as regras da "Experiência Premium".
>
> **Recomendação Propósito:**
> - A estrutura está alinhada com o propósito. Sem mudanças necessárias.

---

## 🔍 3. PESQUISA EXTERNA (Best Practices de Monorepo)

**Fonte:** Pesquisa web sobre estrutura de documentação em monorepos.

**Principais Insights:**
1. ✅ **Top-Level docs folder:** Nossa `GOVERNANCA/` cumpre esse papel.
2. ⚠️ **README.md em cada pasta:** Falta em `curriculo/` e subpastas.
3. ✅ **Convenção de nomes:** Prefixos numéricos são boas práticas.
4. ⚠️ **Pastas temporárias:** `Arrumar/` viola a clareza.

---

## 🎯 4. DECISÕES DA MESA (Consenso)

| # | Ação | Responsável | Prioridade |
|---|------|-------------|------------|
| 1 | Renomear arquivos GOVERNANCA com prefixos (05_, 06_) | DevOps/Design | ALTA |
| 2 | Verificar e limpar pasta `Arrumar/` | Maestro | MÉDIA |
| 3 | Confirmar se `_Assistente_Pessoal/` deve ficar no projeto | Maestro | MÉDIA |
| 4 | Criar `curriculo/README.md` | Pedagogia | BAIXA |

---

## 🚦 5. MENU DE EXECUÇÃO

> **Opção A:** Aplicar apenas as ações de ALTA prioridade (renomear arquivos).
>
> **Opção B:** Aplicar ALTA + perguntar ao Maestro sobre `Arrumar/` e `_Assistente_Pessoal/`.
>
> **Opção C:** Pausar e aguardar aprovação do Maestro para cada item.

---

**AGUARDANDO DECISÃO DO MAESTRO.**
