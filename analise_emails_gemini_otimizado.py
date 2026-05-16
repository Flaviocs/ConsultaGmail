"""
Script OTIMIZADO para analisar emails do Gmail usando Gemini AI
Com controle de quota e processamento em lotes
"""
import os
import base64
import time
import requests
import warnings
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Desabilita warnings de SSL
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def autenticar_gmail():
    """Autentica e retorna o serviço do Gmail"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            try:
                creds = flow.run_local_server(port=0)
            except AttributeError:
                creds = flow.run_console()

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def configurar_gemini():
    """Configura o Gemini com API key"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'sua_chave_aqui':
        raise ValueError(
            '\n❌ GEMINI_API_KEY não configurada!\n'
            '   1. Obtenha sua chave em: https://aistudio.google.com/app/apikey\n'
            '   2. Edite o arquivo .env\n'
            '   3. Cole sua chave API\n'
        )

    return api_key


def extrair_corpo_email(payload):
    """Extrai o corpo do email"""
    corpo = ''
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                corpo = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
            elif part['mimeType'] == 'text/html' and not corpo and 'data' in part['body']:
                corpo = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    elif 'body' in payload and 'data' in payload['body']:
        corpo = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    return corpo[:5000]  # Aumentado para 5000 chars para resumos melhores


def analisar_email_com_gemini(api_key, assunto, remetente, corpo):
    """Analisa o email usando Gemini via REST API"""
    prompt = f"""Analise este email e classifique em: SPAM, IRRELEVANTE ou IMPORTANTE

Email:
- De: {remetente}
- Assunto: {assunto}
- Corpo: {corpo[:3500]}

Critérios:
- SPAM: propaganda não solicitada, phishing, golpes
- IRRELEVANTE: newsletters, promoções, vagas, supermercado, bemol, mrv, mercado livre, santander
- IMPORTANTE: emails pessoais, profissionais, financeiros, viagens, documentos, confirmações, sebrae, sebraeprev, prefeitura, nota fiscal, guararapes, boletos, multas, valentina, autismo, patricia, lello

Responda EXATAMENTE assim:
CLASSIFICAÇÃO: [SPAM/IRRELEVANTE/IMPORTANTE]
TÍTULO: [título/assunto resumido do email em até 15 palavras]
RESUMO: [
- Se IMPORTANTE: escreva UM parágrafo de 4-6 linhas resumindo o conteúdo principal, pontos-chave, informações relevantes e ações necessárias. Seja detalhado e claro.
- Se IRRELEVANTE: escreva 2 -3 linhas explicando brevemente do que se trata (ex: "Newsletter da loja X promovendo desconto de 50%")
- Se SPAM: escreva 1 linha breve do tipo de spam (ex: "Email promocional não solicitado")
]
"""

    try:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}'

        headers = {'Content-Type': 'application/json'}

        payload = {
            'contents': [{
                'parts': [{'text': prompt}]
            }]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)

        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            return text.strip()
        elif response.status_code == 429:
            return 'QUOTA_EXCEDIDA'
        else:
            return f'ERRO: {response.status_code} {response.text[:100]}'

    except Exception as e:
        if '429' in str(e):
            return 'QUOTA_EXCEDIDA'
        return f'ERRO: {str(e)[:100]}'


def extrair_classificacao(resposta):
    """Extrai classificação, título e resumo"""
    if resposta == 'QUOTA_EXCEDIDA':
        return 'QUOTA_EXCEDIDA', '', ''

    linhas = resposta.split('\n')
    classificacao = 'IRRELEVANTE'
    titulo = ''
    resumo = ''

    for linha in linhas:
        if 'CLASSIFICAÇÃO:' in linha:
            classificacao = linha.split('CLASSIFICAÇÃO:')[1].strip()
        elif 'TÍTULO:' in linha:
            titulo = linha.split('TÍTULO:')[1].strip()
        elif 'RESUMO:' in linha:
            # Pega o resto do texto após RESUMO: (pode ter múltiplas linhas)
            idx = resposta.find('RESUMO:')
            if idx != -1:
                resumo = resposta[idx+7:].strip()
            break

    return classificacao, titulo, resumo


def excluir_email(service, email_id):
    """Move email para lixeira"""
    try:
        service.users().messages().trash(userId='me', id=email_id).execute()
        return True
    except:
        return False


def analisar_emails(service, api_key, max_emails, excluir_spam, excluir_irrelevantes):
    """Analisa emails com controle de quota"""

    # Configurações de quota
    max_por_execucao = int(os.getenv('MAX_EMAILS_POR_EXECUCAO', 500))
    delay = int(os.getenv('DELAY_ENTRE_EMAILS', 4))

    # Limita quantidade
    max_emails = min(max_emails, max_por_execucao)

    print(f'\n🔍 Buscando {max_emails} emails...')
    print(f'⏱️  Delay entre análises: {delay}s (controle de quota)\n')

    results = service.users().messages().list(
        userId='me',
        maxResults=max_emails,
        labelIds=['INBOX']
    ).execute()

    messages = results.get('messages', [])
    if not messages:
        print('✅ Caixa de entrada vazia!')
        return

    print(f'📧 Processando {len(messages)} emails...\n')
    print('=' * 80)

    stats = {
        'SPAM': 0, 'IRRELEVANTE': 0, 'IMPORTANTE': 0,
        'SPAM_DEL': 0, 'IRREL_DEL': 0, 'PROCESSADOS': 0
    }

    for idx, message in enumerate(messages, 1):
        msg = service.users().messages().get(
            userId='me', id=message['id'], format='full'
        ).execute()

        headers = msg['payload']['headers']
        assunto = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sem assunto')
        remetente = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconhecido')
        data = next((h['value'] for h in headers if h['name'] == 'Date'), 'Data desconhecida')
        corpo = extrair_corpo_email(msg['payload'])

        print(f'\n📨 {idx}/{len(messages)}')
        print(f'De: {remetente[:60]}')
        print(f'Assunto: {assunto[:60]}')
        print(f'Data: {data[:60]}')
        print('🤖 Analisando...', end=' ', flush=True)

        resposta = analisar_email_com_gemini(api_key, assunto, remetente, corpo)
        classificacao, titulo, resumo = extrair_classificacao(resposta)

        if classificacao == 'QUOTA_EXCEDIDA':
            print('⚠️  QUOTA EXCEDIDA!')
            print(f'\n   Processados: {stats["PROCESSADOS"]}/{len(messages)}')
            print('   Execute novamente mais tarde para continuar.')
            break

        stats['PROCESSADOS'] += 1

        # Mostra título para todos
        if titulo:
            print(f'   📌 {titulo}')

        if classificacao == 'SPAM':
            print('   🚨 SPAM')
            if resumo:
                print(f'   💬 {resumo}')
            stats['SPAM'] += 1
            if excluir_spam and excluir_email(service, message['id']):
                print('   🗑️  Excluído!')
                stats['SPAM_DEL'] += 1

        elif classificacao == 'IRRELEVANTE':
            print('   📭 IRRELEVANTE')
            if resumo:
                print(f'   💬 {resumo}')
            stats['IRRELEVANTE'] += 1
            if excluir_irrelevantes and excluir_email(service, message['id']):
                print('   🗑️  Excluído!')
                stats['IRREL_DEL'] += 1

        elif classificacao == 'IMPORTANTE':
            print('   ⭐ IMPORTANTE')
            if resumo:
                # Formata resumo com quebras de linha para importantes
                print(f'   📝 Resumo:')
                for linha in resumo.split('\n'):
                    if linha.strip():
                        print(f'      {linha.strip()}')
            stats['IMPORTANTE'] += 1

        print('-' * 80)

        # Delay para não atingir quota
        if idx < len(messages):
            time.sleep(delay)

    # Resumo final
    print(f'\n📊 RESUMO:')
    print(f'   Processados: {stats["PROCESSADOS"]}/{len(messages)}')
    print(f'   ⭐ Importantes: {stats["IMPORTANTE"]}')
    print(f'   📭 Irrelevantes: {stats["IRRELEVANTE"]} (excluídos: {stats["IRREL_DEL"]})')
    print(f'   🚨 Spam: {stats["SPAM"]} (excluídos: {stats["SPAM_DEL"]})')
    total_del = stats['SPAM_DEL'] + stats['IRREL_DEL']
    if total_del > 0:
        print(f'\n   🗑️  TOTAL EXCLUÍDOS: {total_del}')


def main():
    print('=' * 80)
    print('🤖 ANÁLISE INTELIGENTE DE EMAILS - Versão Otimizada')
    print('=' * 80)

    # Configura Gemini
    print('\n⚙️  Configurando Gemini AI...')
    try:
        api_key = configurar_gemini()
        print('✅ Gemini configurado!')
    except ValueError as e:
        print(e)
        return

    # Autentica Gmail
    print('\n⚙️  Autenticando no Gmail...')
    service = autenticar_gmail()
    print('✅ Gmail autenticado!')

    # Configurações
    print('\n' + '=' * 80)
    print('⚙️  CONFIGURAÇÃO')
    print('=' * 80)

    max_execucao = int(os.getenv('MAX_EMAILS_POR_EXECUCAO', 500))
    print(f'\n⚠️  Limite por execução: {max_execucao} emails (controle de quota)')
    print('   (Edite MAX_EMAILS_POR_EXECUCAO no .env para alterar)')

    excluir_spam = input('\n❓ Excluir SPAM automaticamente? (s/n): ').lower() == 's'
    excluir_irrelevantes = input('❓ Excluir IRRELEVANTES automaticamente? (s/n): ').lower() == 's'

    try:
        qtd = int(input(f'\n❓ Quantos emails analisar? (max {max_execucao}): ') or max_execucao)
    except:
        qtd = max_execucao

    print('\n' + '=' * 80)

    # Analisa
    analisar_emails(service, api_key, qtd, excluir_spam, excluir_irrelevantes)

    print('\n' + '=' * 80)
    print('✅ Concluído!')
    print('=' * 80)


if __name__ == '__main__':
    main()
