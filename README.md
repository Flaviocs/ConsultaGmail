# 📧 Análise Inteligente de Emails com Gemini AI

Script Python para analisar emails do Gmail usando inteligência artificial do Gemini, classificando-os automaticamente em **SPAM**, **IRRELEVANTE** ou **IMPORTANTE**, com exclusão automática opcional.

## ✨ Funcionalidades

- 🤖 **Análise com IA**: Usa Gemini 2.5 Flash para classificar emails
- 🏷️ **Classificação em 3 categorias**: SPAM, IRRELEVANTE ou IMPORTANTE
- 📝 **Resumos inteligentes**: Gera resumos detalhados (4-6 linhas) para emails importantes
- 📅 **Informações completas**: Exibe remetente, assunto e data de recebimento
- 🗑️ **Exclusão automática**: Remove spam e emails irrelevantes opcionalmente
- 🕒 **Exclusão por idade**: Remove emails com mais de X dias utilizando a data interna do Gmail
- 🛡️ **Resiliência na IA**: Tratamento robusto com fallback caso ocorra instabilidade ou erro na IA
- 🔌 **Integração MCP (Model Context Protocol)**: Servidor pronto para agentes como Hermes Agent e Claude Desktop
- ⚙️ **Processamento em lote**: Analisa até 500 emails por execução
- 📊 **Estatísticas detalhadas**: Mostra resumo completo da análise com contadores
- ⏱️ **Controle de quota**: Delay configurável entre análises

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Conta Google/Gmail
- API Key do Gemini (gratuita)

## 🚀 Instalação

### 1. Clone ou baixe o projeto

```bash
cd ConsultaGmail
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Gmail (OAuth 2.0)

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a **Gmail API**:
   - Vá em "APIs e Serviços" > "Biblioteca"
   - Busque por "Gmail API"
   - Clique em "Ativar"
4. Crie credenciais OAuth 2.0:
   - Vá em "APIs e Serviços" > "Credenciais"
   - Clique em "Criar credenciais" > "ID do cliente OAuth"
   - Tipo de aplicativo: **Aplicativo para computador**
   - Dê um nome (ex: "Consulta Gmail")
5. Baixe o arquivo JSON de credenciais
6. Renomeie o arquivo para `credentials.json`
7. Coloque na pasta raiz do projeto

**Importante:** Na primeira execução, o navegador abrirá para você autorizar o acesso ao Gmail. Um arquivo `token.json` será gerado automaticamente.

### 5. Configure o Gemini AI

1. Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Clique em "Create API Key"
3. Copie a chave gerada
4. Crie um arquivo `.env` na raiz do projeto (você pode copiar `.env.example`):
   ```bash
   cp .env.example .env
   ```
5. Edite o arquivo `.env` e cole sua chave:
   ```bash
   GEMINI_API_KEY=sua_chave_api_aqui
   ```

## 🎯 Como Usar

### Script Principal (Recomendado)

```bash
python analise_emails_gemini_otimizado.py
```

**O que ele faz:**

1. ✅ Autentica no Gmail (OAuth 2.0)
2. ✅ Configura Gemini AI
3. ❓ Pergunta se deseja excluir SPAM automaticamente
4. ❓ Pergunta se deseja excluir IRRELEVANTES automaticamente
5. ❓ Pergunta se deseja excluir emails com mais de quantos dias (0 para desconsiderar)
6. ❓ Pergunta quantos emails analisar (máx: 500 por execução)
7. 🤖 Analisa cada email com Gemini 2.5 Flash
8. 📊 Mostra: remetente, assunto, data, título resumido, classificação e resumo
9. 🗑️ Exclui conforme configurado (spam, irrelevantes e/ou idade)
10. 📈 Apresenta estatísticas finais detalhadas

### Servidor MCP para Agentes (Hermes / Claude / Antigravity)

O projeto inclui um servidor MCP padrão (`mcp_server.py`) que disponibiliza ferramentas para agentes autônomos consultarem a caixa de entrada, realizarem análise com IA e moverem e-mails para a lixeira:

```bash
python mcp_server.py
```

Consulte [HERMES_MCP_CONFIG.md](HERMES_MCP_CONFIG.md) para detalhes de configuração e integração com o Hermes Agent via Telegram.

### Script de Listagem Simples (Opcional)

```bash
python consulta_gmail.py
```

Apenas lista os últimos 50 emails sem análise de IA.

## 📊 Exemplo de Saída

```
================================================================================
🤖 ANÁLISE INTELIGENTE DE EMAILS - Versão Otimizada
================================================================================

⚙️  Configurando Gemini AI...
✅ Gemini configurado!

⚙️  Autenticando no Gmail...
✅ Gmail autenticado!

================================================================================
⚙️  CONFIGURAÇÃO
================================================================================

⚠️  Limite por execução: 500 emails (controle de quota)
   (Edite MAX_EMAILS_POR_EXECUCAO no .env para alterar)

❓ Excluir SPAM automaticamente? (s/n): s
❓ Excluir IRRELEVANTES automaticamente? (s/n): s

❓ Quantos emails analisar? (max 500): 10

================================================================================

🔍 Buscando 10 emails...
⏱️  Delay entre análises: 4s (controle de quota)

📧 Processando 10 emails...

================================================================================

📨 1/10
De: empresa@exemplo.com
Assunto: Reunião importante sobre o projeto Q2
Data: Mon, 15 May 2026 14:30:00 -0300
🤖 Analisando... 
   📌 Reunião projeto Q2 - planejamento trimestral
   ⭐ IMPORTANTE
   📝 Resumo:
      Email convocando reunião estratégica na próxima terça-feira às 14h
      para discutir o planejamento do segundo trimestre. A reunião abordará
      metas de vendas, alocação de recursos e definição de prioridades.
      É necessário confirmar presença até segunda-feira e preparar relatório
      de status do projeto atual para apresentação.
--------------------------------------------------------------------------------

📨 2/10
De: newsletter@loja.com
Assunto: 50% OFF em toda a loja - Fim de Semana
Data: Mon, 15 May 2026 09:15:00 -0300
🤖 Analisando... 
   📌 Promoção de fim de semana - desconto 50%
   📭 IRRELEVANTE
   💬 Newsletter da Loja promovendo desconto de 50% em produtos selecionados
      durante o fim de semana. Válido apenas para compras online.
   🗑️  Excluído!
--------------------------------------------------------------------------------

📨 3/10
De: noreply@spam.com
Assunto: Você ganhou um prêmio! Clique aqui
Data: Sun, 14 May 2026 18:45:00 -0300
🤖 Analisando... 
   📌 Golpe de falso prêmio
   🚨 SPAM
   💬 Email promocional não solicitado tentando phishing
   🗑️  Excluído!
--------------------------------------------------------------------------------

📊 RESUMO:
   Processados: 10/10
   ⭐ Importantes: 3
   📭 Irrelevantes: 5 (excluídos: 5)
   🚨 Spam: 2 (excluídos: 2)

   🗑️  TOTAL EXCLUÍDOS: 7

================================================================================
✅ Concluído!
================================================================================
```

## ⚙️ Configurações (.env)

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```bash
# API Key do Gemini (obrigatório)
GEMINI_API_KEY=sua_chave_aqui

# Configurações opcionais
MAX_EMAILS_POR_EXECUCAO=500   # Máximo por execução (padrão: 500)
DELAY_ENTRE_EMAILS=4          # Segundos entre análises (padrão: 4)
```

**Notas importantes:**

- `GEMINI_API_KEY`: **Obrigatório** - Sua chave da API do Gemini
- `MAX_EMAILS_POR_EXECUCAO`: Controla quantos emails podem ser processados por vez (máximo: 500)
- `DELAY_ENTRE_EMAILS`: Intervalo de espera entre cada análise para evitar exceder quotas da API
- Para processar mais de 500 emails, execute o script múltiplas vezes

## 🎨 Critérios de Classificação

### SPAM 🚨

Emails que devem ser descartados:

- Propaganda não solicitada
- Phishing e golpes
- Ofertas suspeitas
- Emails com links maliciosos

**Resumo gerado**: 1 linha breve identificando o tipo de spam

### IRRELEVANTE 📭

Emails que não são prioritários:

- Newsletters genéricos, feeds e assinaturas (Substack, Morning Call, Radar IA, etc.)
- Notificações de redes sociais e comunidades (Discord, etc.)
- Promoções e ofertas de lojas/serviços (Bemol, MRV, Mercado Livre, Santander, Livelo, Visa, Rappi, Netflix, Sams Club, Adapta, Samsung, Dropbox, Levante, Suno, Sofisa, n8n, AppBarber, etc.)
- Notificações de plataformas de vagas, judiciais ou utilitárias secundárias (Jusbrasil, etc.)

**Resumo gerado**: 2-3 linhas explicando brevemente o conteúdo

### IMPORTANTE ⭐

Emails que merecem sua atenção:

- Emails pessoais e profissionais diretos
- Assuntos financeiros (boletos, multas, extratos relevantes)
- Notas fiscais (Guararapes, etc.)
- Confirmações de viagens e passagens
- Documentos fiscais e contratuais
- Comunicados importantes (Sebrae, SebraePrev, Prefeitura)
- Assuntos específicos e familiares prioritários (Valentina, Autismo, Patricia, Lello)
- Conteúdos e atualizações essenciais sobre Inteligência Artificial ou temas correlatos

**Resumo gerado**: 4-6 linhas detalhadas com pontos-chave, informações relevantes e ações necessárias

## 💰 Limites e Custos

### API Gratuita do Gemini

- ✅ **Modelo**: Gemini 2.5 Flash
- ✅ **Custo**: Totalmente gratuito
- ✅ **Uso**: Perfeito para uso pessoal
- ⚠️ **Limites**: Respeite os limites da API gratuita
- 📊 **Controle**: Delay automático entre requisições

**Dicas:**

- Execute regularmente para manter sua caixa organizada
- Ajuste `DELAY_ENTRE_EMAILS` se encontrar erros de quota
- O script para automaticamente se a quota for excedida
- Processe emails em lotes menores se necessário

## 🔒 Segurança

- ❌ **NUNCA compartilhe**: `credentials.json`, `token.json`, `.env`
- ✅ Arquivos protegidos no `.gitignore`
- ✅ OAuth 2.0 seguro para Gmail
- ✅ API Key do Gemini com restrições opcionais
- ✅ SSL/TLS em todas as comunicações

**Arquivos sensíveis protegidos:**

```
credentials.json  # Credenciais OAuth do Gmail
token.json        # Token de acesso gerado
.env              # Variáveis de ambiente (API Keys)
```

## 🆘 Problemas Comuns

### ❌ "GEMINI_API_KEY não configurada"

**Solução:**

1. Verifique se criou o arquivo `.env` na raiz do projeto
2. Confirme que a chave está no formato: `GEMINI_API_KEY=sua_chave_aqui`
3. Obtenha uma chave em: https://aistudio.google.com/app/apikey

### ❌ "Erro no navegador" (OAuth)

**Solução:**

1. Não feche o navegador antes de completar a autorização
2. Certifique-se que o arquivo `credentials.json` está na raiz
3. Tente excluir `token.json` e autenticar novamente
4. Se persistir, use o método de console (fallback automático)

### ❌ "QUOTA EXCEDIDA"

**Solução:**

1. Você atingiu o limite da API do Gemini
2. Aguarde alguns minutos/horas e tente novamente
3. Aumente o `DELAY_ENTRE_EMAILS` no arquivo `.env`
4. Processe menos emails por vez

### ❌ Resumo não aparece

**Solução:**

1. Certifique-se que a API Key está correta no `.env`
2. Verifique se há erros no console
3. Teste com um único email primeiro
4. Confirme que tem acesso à internet

### ❌ "403 PERMISSION_DENIED"

**Solução:**

1. Verifique se a Gmail API está ativada no Google Cloud Console
2. Recrie as credenciais OAuth se necessário
3. Verifique se a API Key do Gemini não tem restrições bloqueando

## 📁 Estrutura do Projeto

```
ConsultaGmail/
├── analise_emails_gemini_otimizado.py  # Script principal de análise inteligente ⭐
├── consulta_gmail.py                   # Listagem simples sem IA (opcional)
├── gmail_core.py                       # Módulo compartilhado de integração Gmail / IA
├── mcp_server.py                       # Servidor MCP para agentes (Hermes, Claude, etc.)
├── HERMES_MCP_CONFIG.md                # Guia de configuração e comandos do Hermes MCP
├── INSTRUCOES_HERMES.txt               # Instruções complementares para o Hermes
├── requirements.txt                    # Dependências Python
├── .env.example                        # Exemplo de configuração
├── credentials.json                    # OAuth Gmail (você cria) ⚠️
├── token.json                          # Token Gmail (auto gerado) ⚠️
├── .env                               # Configurações (você cria) ⚠️
├── .gitignore                         # Proteção de arquivos sensíveis
├── README.md                          # Este arquivo
└── venv/                              # Ambiente virtual (opcional)

⚠️ = Arquivos sensíveis (não commitar)
```

## 🛠️ Dependências

```
google-api-python-client==2.132.0  # Gmail API
google-auth-httplib2==0.2.0        # Autenticação HTTP
google-auth-oauthlib==1.2.0        # OAuth 2.0
google-genai==1.0.0                # Gemini SDK
python-dotenv==1.0.1               # Variáveis de ambiente
requests==2.32.3                   # Requisições HTTP
urllib3==2.2.1                     # Cliente HTTP
mcp>=1.2.0,<2.0.0                  # SDK do Model Context Protocol
```

## 📚 Documentação e Recursos

- [Gmail API](https://developers.google.com/gmail/api) - Documentação oficial da API do Gmail
- [Gemini API](https://ai.google.dev/docs) - Documentação oficial do Gemini
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) - Especificação do protocolo MCP
- [Google AI Studio](https://aistudio.google.com/) - Console para gerenciar API Keys
- [Google Cloud Console](https://console.cloud.google.com/) - Gerenciamento de projetos e APIs

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Enviar pull requests

## 📝 Licença

Este projeto é de código aberto e está disponível para uso pessoal e educacional.

---

**Desenvolvido com ❤️**

*Última atualização: Outubro 2026*
