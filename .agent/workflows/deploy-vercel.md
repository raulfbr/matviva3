---
description: Como conectar o projeto Matemática Viva ao Vercel para Deploy Automático
---

> [!IMPORTANT]
> **Controle de Commits:** O usuário (Maestro) controla quando fazer commits e push. O Arquiteto AI não deve fazer commits automáticos a cada alteração — apenas quando explicitamente solicitado.

# Deploy Automático no Vercel

Este guia explica como conectar o repositório GitHub do Matemática Viva ao Vercel para atualizações automáticas.

## Pré-requisitos

1.  Ter o código no GitHub (Feito pelo Antigravity ✅).
2.  Conta no [Vercel](https://vercel.com).

## Passo a Passo

1.  **Acesse o Vercel**: Faça login na sua conta.
2.  **Novo Projeto**:
    *   Clique em "Add New..." e selecione "Project".
    *   Na tela "Import Git Repository", encontre o repositório `matematica-viva-v3` (ou o nome que você usou) e clique em **Import**.
3.  **Configurar Build**:
    *   O Vercel deve detectar algumas coisas, mas precisamos ajustar para o nosso gerador Python.
    *   Expanda a seção **Build and Output Settings**.
    *   **Build Command**: Insira este comando exato:
        ```bash
        pip install -r requirements.txt && python scripts/gutenberg.py
        ```
    *   **Output Directory**: Insira:
        ```
        dist/web
        ```
    *   **Install Command**: (Deixe em branco ou padrão).
4.  **Deploy**:
    *   Clique em **Deploy**.
    *   Aguarde o processo. O Vercel vai instalar o Python, rodar nosso script `gutenberg.py` e publicar o site que fica na pasta `dist/web`.

## Como atualizar o site?

Sempre que você (ou o Antigravity) fizer mudanças e rodar o comando `git push origin main` (ou eu fizer isso por você), o Vercel detectará a mudança e atualizará o site automaticamente em 1-2 minutos.
