# 🔐 Configuração OAuth 2.0 para Gmail API

Guia detalhado para configurar a autenticação OAuth 2.0 e acessar sua conta Gmail.

## 📋 Pré-requisitos

- Conta Google/Gmail
- Navegador web
- Projeto criado no Google Cloud Console

## 🚀 Passo a Passo

### 1. Acesse o Google Cloud Console

Acesse: [https://console.cloud.google.com/](https://console.cloud.google.com/)

### 2. Crie ou Selecione um Projeto

1. No topo da página, clique no seletor de projeto
2. Clique em "Novo Projeto"
3. Digite um nome (ex: "Consulta Gmail")
4. Clique em "Criar"
5. Aguarde a criação do projeto (alguns segundos)

### 3. Ative a Gmail API

1. No menu lateral, vá em **"APIs e Serviços"** > **"Biblioteca"**
2. Na barra de busca, digite: `Gmail API`
3. Clique em "Gmail API" nos resultados
4. Clique no botão **"Ativar"**
5. Aguarde a ativação (alguns segundos)

### 4. Configure a Tela de Consentimento OAuth

1. No menu lateral, vá em **"APIs e Serviços"** > **"Tela de consentimento OAuth"**
2. Selecione **"Externo"** (para uso pessoal)
3. Clique em **"Criar"**
4. Preencha as informações obrigatórias:
   - **Nome do app**: Ex: "Consulta Gmail"
   - **Email de suporte do usuário**: Seu email
   - **Email do desenvolvedor**: Seu email
5. Clique em **"Salvar e continuar"**
6. Em "Escopos", clique em **"Salvar e continuar"** (não precisa adicionar escopos aqui)
7. Em "Usuários de teste", clique em **"+ Adicionar usuários"**
   - Digite seu email do Gmail
   - Clique em "Adicionar"
8. Clique em **"Salvar e continuar"**
9. Revise as informações e clique em **"Voltar ao painel"**

### 5. Crie as Credenciais OAuth 2.0

1. No menu lateral, vá em **"APIs e Serviços"** > **"Credenciais"**
2. Clique em **"Criar credenciais"** (botão azul no topo)
3. Selecione **"ID do cliente OAuth"**
4. Tipo de aplicativo: Selecione **"Aplicativo para computador"**
5. Nome: Digite um nome (ex: "Cliente Desktop Gmail")
6. Clique em **"Criar"**

### 6. Baixe o Arquivo de Credenciais

1. Uma janela aparecerá com "Cliente OAuth criado"
2. Clique no botão **"Fazer download do JSON"**
3. Salve o arquivo
4. **IMPORTANTE**: Renomeie o arquivo baixado para: `credentials.json`
5. Mova o arquivo `credentials.json` para a pasta raiz do projeto `ConsultaGmail/`

### 7. Estrutura do credentials.json

O arquivo deve ter uma estrutura similar a esta:

```json
{
  "installed": {
    "client_id": "123456789-abcdefghijk.apps.googleusercontent.com",
    "project_id": "seu-projeto-12345",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "ABC-DEF123_xyz789",
    "redirect_uris": ["http://localhost"]
  }
}
```

## 🎯 Primeira Execução

### Processo de Autorização

Na primeira vez que executar o script:

```bash
python analise_emails_gemini_otimizado.py
```

1. **Navegador abrirá automaticamente**
2. Selecione sua conta Google
3. Você verá um aviso: "Google ainda não verificou este app"
   - Clique em **"Avançado"**
   - Clique em **"Acessar [nome do app] (não seguro)"**
4. Na tela de permissões, revise o que será permitido:
   - ✅ Ver, compor, enviar e excluir permanentemente todos os seus e-mails do Gmail
5. Clique em **"Continuar"**
6. Você verá: "A autenticação foi bem-sucedida"
7. Pode fechar o navegador

### Token Gerado

- Um arquivo `token.json` será criado automaticamente
- Este arquivo armazena seu token de acesso
- **NÃO compartilhe este arquivo**
- Ele permite acesso à sua conta sem precisar autenticar novamente

## 🔄 Renovação do Token

O token expira após algum tempo. Quando isso acontecer:

1. O script tentará renovar automaticamente
2. Se falhar, exclua o `token.json`:
   ```bash
   rm token.json  # Linux/Mac
   del token.json  # Windows
   ```
3. Execute o script novamente
4. Um novo processo de autorização será iniciado

## ⚠️ Avisos de Segurança

### "App não verificado"

Este aviso aparece porque você criou um app OAuth pessoal que não foi revisado pelo Google. Isso é **normal e seguro** para apps de uso pessoal.

**Não se preocupe!** Você é o desenvolvedor e o único usuário do app.

### Permissões Solicitadas

O app solicita acesso para:

- **Ler emails**: Para listar e analisar mensagens
- **Modificar emails**: Para marcar como lido/não lido
- **Excluir emails**: Para mover para lixeira (spam/irrelevantes)

**Todas as operações são executadas localmente no seu computador.**

## 🛡️ Segurança

### Proteja seus arquivos

**NUNCA compartilhe:**

- ❌ `credentials.json` - Credenciais OAuth do seu projeto
- ❌ `token.json` - Token de acesso à sua conta
- ❌ `.env` - Chaves de API

**Verificações de segurança:**

```bash
# Verifique se está no .gitignore
cat .gitignore

# Deve conter:
credentials.json
token.json
.env
```

### Revogando Acesso

Se precisar revogar o acesso do app:

1. Acesse: [https://myaccount.google.com/permissions](https://myaccount.google.com/permissions)
2. Encontre o app "Consulta Gmail" (ou nome que você deu)
3. Clique em **"Remover acesso"**
4. Exclua os arquivos:
   ```bash
   rm credentials.json token.json
   ```

## 🆘 Problemas Comuns

### ❌ "Arquivo credentials.json não encontrado"

**Solução:**

- Certifique-se que o arquivo está na pasta raiz do projeto
- Verifique se o nome está correto: `credentials.json` (não `credentials (1).json`)

### ❌ "Navegador não abre"

**Solução:**

- O script tentará usar autenticação via console automaticamente
- Copie a URL exibida no terminal
- Cole no navegador manualmente
- Complete a autorização
- Copie o código de autorização de volta para o terminal

### ❌ "Error: redirect_uri_mismatch"

**Solução:**

1. Vá em Google Cloud Console > Credenciais
2. Edite o cliente OAuth
3. Em "URIs de redirecionamento autorizados", adicione:
   - `http://localhost:8080/`
   - `http://localhost`

### ❌ "Access denied"

**Solução:**

1. Verifique se adicionou seu email como "usuário de teste" na tela de consentimento
2. Use o mesmo email da conta Gmail que deseja acessar

### ❌ "Token has been expired or revoked"

**Solução:**

```bash
# Exclua o token antigo
rm token.json

# Execute novamente
python analise_emails_gemini_otimizado.py
```

## 📚 Recursos Adicionais

- [Documentação OAuth 2.0 do Google](https://developers.google.com/identity/protocols/oauth2)
- [Gmail API - Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [Google Cloud Console](https://console.cloud.google.com/)

## ✅ Checklist de Configuração

- [ ] Projeto criado no Google Cloud Console
- [ ] Gmail API ativada
- [ ] Tela de consentimento OAuth configurada
- [ ] Email adicionado como usuário de teste
- [ ] Credenciais OAuth criadas (tipo: Aplicativo para computador)
- [ ] Arquivo `credentials.json` baixado e renomeado
- [ ] Arquivo `credentials.json` na pasta raiz do projeto
- [ ] Primeira autenticação concluída com sucesso
- [ ] Arquivo `token.json` gerado automaticamente
- [ ] Script executa sem erros de autenticação

---

**🎉 Pronto! Seu acesso ao Gmail está configurado!**

Volte para o [README.md](README.md) para continuar a configuração.
