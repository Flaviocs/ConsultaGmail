# 🤖 Configuração da API do Gemini

Guia detalhado para obter e configurar sua API Key do Gemini para análise de emails com IA.

## 📋 Pré-requisitos

- Conta Google
- Navegador web
- Acesso ao Google AI Studio

## 🚀 Passo a Passo

### 1. Acesse o Google AI Studio

Acesse: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 2. Faça Login

- Use sua conta Google para fazer login
- Aceite os Termos de Serviço se aparecer

### 3. Crie uma API Key

1. Clique no botão **"Create API Key"** ou **"Criar chave de API"**
2. Você terá duas opções:

   **Opção A: Criar chave em novo projeto**
   - Clique em "Create API key in new project"
   - Um novo projeto será criado automaticamente
   - Uma chave será gerada

   **Opção B: Usar projeto existente**
   - Clique em "Create API key"
   - Selecione um projeto existente do Google Cloud
   - Uma chave será gerada

3. A chave será exibida na tela
4. Clique no ícone de **copiar** para copiar a chave

### 4. Salve a API Key

**IMPORTANTE:** Esta é a única vez que você verá a chave completa!

- A chave tem formato: `AIzaSy...` (cerca de 39 caracteres)
- Guarde em local seguro
- Se perder, terá que criar uma nova

### 5. Configure o Projeto

#### Crie o arquivo .env

Na pasta raiz do projeto `ConsultaGmail/`, crie um arquivo chamado `.env`:

**Linux/Mac:**
```bash
touch .env
```

**Windows (PowerShell):**
```powershell
New-Item -Path .env -ItemType File
```

**Windows (CMD):**
```cmd
type nul > .env
```

#### Adicione a chave no .env

Abra o arquivo `.env` com um editor de texto e adicione:

```bash
# API Key do Gemini (gratuita)
# Obtenha em: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=AIzaSy_COLE_SUA_CHAVE_AQUI

# Configurações opcionais
MAX_EMAILS_POR_EXECUCAO=500
DELAY_ENTRE_EMAILS=4
```

**Substitua** `AIzaSy_COLE_SUA_CHAVE_AQUI` pela sua chave real copiada no passo 3.

#### Exemplo de .env configurado

```bash
GEMINI_API_KEY=AIzaSyBnC8_x4Y2ZmRpQ1wL5kJ3hD9fG7tN6vM8
MAX_EMAILS_POR_EXECUCAO=500
DELAY_ENTRE_EMAILS=4
```

## ✅ Verificação

### Teste a configuração

Execute o script:

```bash
python analise_emails_gemini_otimizado.py
```

Se a configuração estiver correta, você verá:

```
⚙️  Configurando Gemini AI...
✅ Gemini configurado!
```

### Erros comuns

#### ❌ "GEMINI_API_KEY não configurada"

```
❌ GEMINI_API_KEY não configurada!
   1. Obtenha sua chave em: https://aistudio.google.com/app/apikey
   2. Edite o arquivo .env
   3. Cole sua chave API
```

**Solução:**

1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Verifique se a linha `GEMINI_API_KEY=...` está presente
3. Verifique se não há espaços antes ou depois do `=`
4. Certifique-se que não está usando `sua_chave_aqui` como valor

#### ❌ "ERRO: 403" ou "PERMISSION_DENIED"

**Solução:**

1. Verifique se a chave foi copiada corretamente (sem espaços extras)
2. Tente criar uma nova chave no Google AI Studio
3. Certifique-se que a API do Gemini está disponível na sua região

#### ❌ "ERRO: 429" ou "QUOTA_EXCEDIDA"

**Solução:**

- Você excedeu o limite de requisições da API gratuita
- Aguarde alguns minutos/horas antes de tentar novamente
- Aumente o valor de `DELAY_ENTRE_EMAILS` no `.env`

## 💰 Limites da API Gratuita

### Modelo Gemini 2.5 Flash

- ✅ **Totalmente gratuito**
- ✅ Limite generoso de requisições por minuto
- ✅ Perfeito para uso pessoal
- ⚠️ Pode ter limitações em horários de pico

### Boas Práticas

1. **Use delays entre requisições:**
   - Configure `DELAY_ENTRE_EMAILS=4` (4 segundos)
   - Evita atingir limites de taxa

2. **Processe em lotes:**
   - Não tente processar 500 emails de uma vez se não for necessário
   - Divida em lotes menores (ex: 50-100 por vez)

3. **Monitore o uso:**
   - Fique atento a mensagens de "QUOTA_EXCEDIDA"
   - Ajuste o delay se necessário

## 🔐 Segurança da API Key

### Proteja sua chave

**NUNCA:**

- ❌ Compartilhe sua API Key publicamente
- ❌ Faça commit do arquivo `.env` no Git
- ❌ Publique a chave em fóruns, chat, redes sociais
- ❌ Envie a chave por email ou mensagem

**SEMPRE:**

- ✅ Mantenha a chave no arquivo `.env`
- ✅ Verifique que `.env` está no `.gitignore`
- ✅ Use variáveis de ambiente
- ✅ Revogue chaves expostas imediatamente

### Verificar .gitignore

```bash
# Verifique se .env está protegido
cat .gitignore

# Deve conter:
.env
credentials.json
token.json
```

### Revogar uma chave comprometida

Se sua chave foi exposta:

1. Acesse: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Encontre a chave comprometida
3. Clique no ícone de **lixeira** para excluir
4. Crie uma nova chave
5. Atualize o arquivo `.env` com a nova chave

## 📊 Gerenciamento de Chaves

### Listar suas chaves

1. Acesse: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Veja todas as chaves criadas
3. Cada chave mostra:
   - Nome (se definido)
   - Projeto associado
   - Data de criação
   - Últimos 4 caracteres

### Criar múltiplas chaves

Você pode ter várias chaves para diferentes projetos:

```bash
# .env para projeto de emails
GEMINI_API_KEY=AIzaSyBnC8_x4Y2ZmRpQ...

# .env para outro projeto
GEMINI_API_KEY=AIzaSyDfE9_a5B3CpNrS...
```

### Adicionar restrições (opcional)

Para maior segurança, você pode restringir o uso da chave:

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Vá em "APIs e Serviços" > "Credenciais"
3. Clique na chave de API
4. Em "Restrições de aplicativo":
   - **Endereços IP**: Restrinja a IPs específicos
   - **Sites**: Restrinja a domínios específicos
5. Em "Restrições de API":
   - Selecione "Restringir chave"
   - Marque apenas "Generative Language API"

**Nota:** Restrições podem causar erros 403. Use apenas se souber o que está fazendo.

## 🆘 Problemas Comuns

### ❌ Chave não funciona

**Soluções:**

1. Verifique se copiou a chave completa (sem espaços)
2. Tente criar uma nova chave
3. Verifique se está usando o modelo correto (gemini-2.5-flash)
4. Aguarde 1-2 minutos após criar a chave (propagação)

### ❌ Erro de quota

**Soluções:**

1. Aguarde alguns minutos antes de tentar novamente
2. Aumente `DELAY_ENTRE_EMAILS` no `.env`
3. Processe menos emails por vez
4. Distribua o processamento ao longo do dia

### ❌ Arquivo .env não é lido

**Soluções:**

1. Verifique se o arquivo está na **raiz do projeto**
2. Verifique o nome: `.env` (começa com ponto)
3. No Windows, use: `ren env.txt .env` se necessário
4. Confirme que não há extensão oculta (.env.txt)

## 🔄 Atualizações

### Mudança de modelo

O projeto atualmente usa `gemini-2.5-flash`. Se precisar mudar:

**Arquivo:** `analise_emails_gemini_otimizado.py`

```python
# Linha 103 - Altere o modelo aqui
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}'

# Para mudar para outro modelo:
# gemini-2.0-flash-exp
# gemini-1.5-flash
# gemini-1.5-pro
```

**Modelos disponíveis:** [Lista de modelos Gemini](https://ai.google.dev/models/gemini)

## 📚 Recursos Adicionais

- [Google AI Studio](https://aistudio.google.com/) - Console de gerenciamento
- [Documentação Gemini API](https://ai.google.dev/docs) - Documentação oficial
- [Modelos disponíveis](https://ai.google.dev/models/gemini) - Lista de modelos
- [Limites e quotas](https://ai.google.dev/pricing) - Informações sobre limites

## ✅ Checklist de Configuração

- [ ] Conta Google criada/existente
- [ ] Acessou o Google AI Studio
- [ ] API Key criada com sucesso
- [ ] Chave copiada e salva em local seguro
- [ ] Arquivo `.env` criado na raiz do projeto
- [ ] Variável `GEMINI_API_KEY` configurada no `.env`
- [ ] Arquivo `.env` está no `.gitignore`
- [ ] Script executa sem erros de configuração
- [ ] Testes iniciais bem-sucedidos

---

**🎉 Pronto! Sua API do Gemini está configurada!**

Volte para o [README.md](README.md) para começar a usar o script.
