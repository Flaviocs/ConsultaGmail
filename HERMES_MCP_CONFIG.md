# 🚀 Configuração do Servidor MCP para o Hermes Agent

Este guia explica como registrar e integrar o servidor MCP do **ConsultaGmail** no seu agente **Hermes** para que você possa consultar, analisar e gerenciar seus e-mails via Telegram.

---

## 📌 Ferramentas Disponíveis no MCP

O servidor disponibiliza 3 ferramentas (*tools*) prontas para uso da IA:

1. **`listar_ultimos_emails`**: Retorna assunto, remetente e data dos e-mails recentes (Sem uso de IA, execução rápida).
2. **`analisar_caixa_entrada`**: Analisa e-mails usando **Gemini 2.5 Flash**, classifica em `IMPORTANTE`, `IRRELEVANTE` ou `SPAM`, gera resumos e opcionalmente apaga spams/irrelevantes.
3. **`mover_email_para_lixeira`**: Move um e-mail específico para a lixeira do Gmail informando o seu `email_id`.

---

## ⚙️ Exemplo de Configuração JSON (MCP Client)

A maioria das plataformas de agentes MCP (como Hermes, Claude Desktop, Cursor, Antigravity) aceita a inclusão de um servidor MCP no formato JSON abaixo:

```json
{
  "mcpServers": {
    "gmail-ai-analyzer": {
      "command": "python",
      "args": [
        "c:/Users/Flaviocs/Documents/PessoalDev/ConsultaGmail/mcp_server.py"
      ],
      "cwd": "c:/Users/Flaviocs/Documents/PessoalDev/ConsultaGmail"
    }
  }
}
```

> **Nota:** Se você utiliza um ambiente virtual (`venv`), substitua `"command": "python"` pelo caminho do executável Python no ambiente virtual, por exemplo:
> `"c:/Users/Flaviocs/Documents/PessoalDev/ConsultaGmail/venv/Scripts/python.exe"`

---

## 🤖 Como Usar pelo Telegram com o Hermes

Com o MCP conectado ao Hermes, você pode enviar comandos em linguagem natural no chat do Telegram, como:

- 💬 *"Hermes, veja quais foram os últimos 5 e-mails que recebi no Gmail."*
- 💬 *"Analise os meus 10 últimos e-mails do Gmail e me mande o resumo dos que forem IMPORTANTES."*
- 💬 *"Hermes, analise a caixa de entrada e limpe todos os SPAMs automaticamente."*
- 💬 *"Mova o e-mail de ID '18f23a9b4c0d1234' para a lixeira."*

---

## 🔐 Requisitos de Credenciais e Arquivos

Certifique-se de que a pasta `ConsultaGmail` possui os arquivos de configuração necessários:
- `credentials.json` (OAuth 2.0 do Gmail Client)
- `token.json` (Token de autorização gerado previamente)
- `.env` (Com as chaves e o caminho para o arquivo de credenciais GCP/Vertex AI)
