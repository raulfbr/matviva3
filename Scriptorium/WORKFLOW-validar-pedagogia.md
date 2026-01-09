---
description: Validar conteúdo pedagógico usando validadores Python
---

# Validação Pedagógica

Executa validadores Charlotte Mason, Singapura CPA e C.S. Lewis.

## Teste Rápido

// turbo
1. Rodar testes standalone:
```bash
cd WorkFlow && python mcp_server/server.py --test
```

## Validar Texto Interativo

2. Abrir Python e importar:
```python
from validators import validate_living_style, validate_cpa_compliance, check_lewis_style

# Charlotte Mason
result = validate_living_style("Seu texto...")

# CPA (fase: CONCRETE, PICTORIAL, ABSTRACT)
result = validate_cpa_compliance("Texto...", "CONCRETE")

# Lewis
result = check_lewis_style("Diálogo Guardião...")
```

## Critérios de Aprovação

| Validador | Score Mínimo | Regra Principal |
|-----------|-------------|-----------------|
| Charlotte Mason | 80/100 | Sem bullets, vocabulário rico |
| Singapura CPA | 80/100 | Respeitar fase |
| C.S. Lewis | 70/100 | Usar analogias |
