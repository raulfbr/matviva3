# WorkFlow - Sistema de Validação Pedagógica

Sistema de validação automatizada baseado em Google ADK e MCP para garantir conformidade pedagógica com as filosofias Charlotte Mason, Singapura CPA e C.S. Lewis.

## Estrutura

```
WorkFlow/
├── validators/      # Validadores Python
├── mcp_server/      # Servidor MCP
├── corpus/          # Corpora de referência
└── tests/           # Testes automatizados
```

## Uso Rápido

```bash
# Instalar dependências
pip install -r mcp_server/requirements.txt

# Iniciar servidor MCP
python mcp_server/server.py
```

## Documentação

- [DeepSearchWorkFlow.md](./DeepSearchWorkFlow.md) - Pesquisa original
- [Validadores](./validators/README.md) - Documentação dos validadores
