"""
Módulo Core para autenticação, consulta e análise de e-mails do Gmail com Gemini AI.
Fornece funções reutilizáveis e não-interativas para CLI, MCP ou APIs REST.
"""
import os
import base64
import time
import requests
import warnings
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Desabilita warnings de SSL se necessário
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def autenticar_gmail(credentials_path='credentials.json', token_path='token.json'):
    """Autentica e retorna o serviço do Gmail Client API"""
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Arquivo de credenciais OAuth '{credentials_path}' não encontrado.")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            try:
                creds = flow.run_local_server(port=0)
            except AttributeError:
                creds = flow.run_console()

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds, static_discovery=False)


def configurar_gemini():
    """Configura credenciais do Vertex AI via Service Account"""
    credentials_file = os.getenv('GCP_CREDENTIALS_FILE')
    if not credentials_file or not os.path.exists(credentials_file):
        raise ValueError(
            f'Arquivo de credenciais GCP não encontrado: {credentials_file}. '
            'Defina GCP_CREDENTIALS_FILE no arquivo .env.'
        )

    creds = service_account.Credentials.from_service_account_file(
        credentials_file,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    return creds


def extrair_corpo_email(payload):
    """Extrai o corpo do e-mail do payload retornado pela Gmail API"""
    corpo = ''
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                corpo = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                break
            elif part['mimeType'] == 'text/html' and not corpo and 'data' in part['body']:
                corpo = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
    elif 'body' in payload and 'data' in payload['body']:
        corpo = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
    return corpo[:5000]


def analisar_email_com_gemini(creds, assunto, remetente, corpo):
    """Realiza a chamada HTTP para o Vertex AI Gemini model"""
    prompt = f"""Analise este email e classifique em: SPAM, IRRELEVANTE ou IMPORTANTE

Email:
- De: {remetente}
- Assunto: {assunto}
- Corpo: {corpo[:3500]}

Critérios:
- SPAM: propaganda não solicitada, phishing, golpes
- IRRELEVANTE: newsletters, promoções, vagas, supermercado, bemol, mrv, mercado livre, santander, privacy, open-gsd
- IMPORTANTE: emails pessoais, profissionais, financeiros, viagens, documentos, confirmações, sebrae, sebraeprev, prefeitura, nota fiscal, guararapes, boletos, multas, valentina, autismo, patricia, lello, informações sobre inteligencia artificial ou assusntos relacionados

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
        if not creds.valid:
            creds.refresh(Request())

        project = os.getenv('GCP_PROJECT_ID')
        location = os.getenv('GCP_LOCATION', 'us-central1')
        model = 'gemini-2.5-flash'
        url = (
            f'https://{location}-aiplatform.googleapis.com/v1/projects/{project}'
            f'/locations/{location}/publishers/google/models/{model}:generateContent'
        )

        headers = {
            'Authorization': f'Bearer {creds.token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'contents': [{
                'role': 'user',
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
            return f'ERRO: {response.status_code} {response.text[:200]}'

    except Exception as e:
        if '429' in str(e):
            return 'QUOTA_EXCEDIDA'
        return f'ERRO: {str(e)[:100]}'


def extrair_classificacao(resposta):
    """Extrai a classificação, título e resumo da resposta em texto do Gemini"""
    if resposta == 'QUOTA_EXCEDIDA':
        return 'QUOTA_EXCEDIDA', '', ''

    if resposta.startswith('ERRO:'):
        return 'ERRO_API', '', ''

    linhas = resposta.split('\n')
    classificacao = None
    titulo = ''
    resumo = ''

    for linha in linhas:
        linha_limpa = linha.replace('**', '').strip()
        if 'CLASSIFICAÇÃO:' in linha_limpa or 'CLASSIFICACAO:' in linha_limpa:
            partes = linha_limpa.split(':')
            if len(partes) > 1:
                valor = partes[1].strip().strip('[]').strip()
                if valor in ('SPAM', 'IRRELEVANTE', 'IMPORTANTE'):
                    classificacao = valor
        elif 'TÍTULO:' in linha_limpa or 'TITULO:' in linha_limpa:
            partes = linha_limpa.split(':')
            if len(partes) > 1:
                titulo = partes[1].strip().strip('[]')
        elif 'RESUMO:' in linha_limpa:
            idx = resposta.find('RESUMO:')
            if idx != -1:
                resumo = resposta[idx+7:].strip()
            break

    if classificacao is None:
        classificacao = 'IRRELEVANTE'

    return classificacao, titulo, resumo


def excluir_email(service, email_id):
    """Move e-mail para a lixeira no Gmail"""
    try:
        service.users().messages().trash(userId='me', id=email_id).execute()
        return True
    except Exception:
        return False


def listar_ultimos_emails_metadados(service, max_results=10):
    """Lista metadados dos últimos e-mails da Inbox sem usar Gemini (rápido)"""
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results,
        labelIds=['INBOX']
    ).execute()

    messages = results.get('messages', [])
    lista = []

    for msg_meta in messages:
        msg = service.users().messages().get(
            userId='me',
            id=msg_meta['id'],
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()

        headers = msg.get('payload', {}).get('headers', [])
        assunto = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sem assunto')
        remetente = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconhecido')
        data = next((h['value'] for h in headers if h['name'] == 'Date'), 'Data desconhecida')

        lista.append({
            'id': msg_meta['id'],
            'remetente': remetente,
            'assunto': assunto,
            'data': data
        })

    return lista


def analisar_caixa_entrada_dados(service, creds, max_emails=10, excluir_spam=False, excluir_irrelevantes=False):
    """Analisa caixa de entrada e retorna dicionário com resultados detalhados e estatísticas"""
    delay = int(os.getenv('DELAY_ENTRE_EMAILS', 4))
    max_por_execucao = int(os.getenv('MAX_EMAILS_POR_EXECUCAO', 500))
    max_emails = min(max_emails, max_por_execucao)

    results = service.users().messages().list(
        userId='me',
        maxResults=max_emails,
        labelIds=['INBOX']
    ).execute()

    messages = results.get('messages', [])
    if not messages:
        return {
            'mensagens': [],
            'estatisticas': {
                'processados': 0,
                'importantes': 0,
                'irrelevantes': 0,
                'spam': 0,
                'excluidos': 0
            },
            'status': 'caixa_vazia'
        }

    emails_processados = []
    stats = {
        'processados': 0,
        'importantes': 0,
        'irrelevantes': 0,
        'spam': 0,
        'excluidos': 0
    }

    status_geral = 'sucesso'

    for idx, message in enumerate(messages, 1):
        msg = service.users().messages().get(
            userId='me', id=message['id'], format='full'
        ).execute()

        headers = msg.get('payload', {}).get('headers', [])
        assunto = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sem assunto')
        remetente = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconhecido')
        data = next((h['value'] for h in headers if h['name'] == 'Date'), 'Data desconhecida')
        corpo = extrair_corpo_email(msg.get('payload', {}))

        resposta = analisar_email_com_gemini(creds, assunto, remetente, corpo)
        classificacao, titulo, resumo = extrair_classificacao(resposta)

        if classificacao == 'QUOTA_EXCEDIDA':
            status_geral = 'quota_excedida'
            break

        if classificacao == 'ERRO_API':
            if idx < len(messages):
                time.sleep(delay)
            continue

        stats['processados'] += 1
        excluido = False

        if classificacao == 'SPAM':
            stats['spam'] += 1
            if excluir_spam and excluir_email(service, message['id']):
                excluido = True
                stats['excluidos'] += 1

        elif classificacao == 'IRRELEVANTE':
            stats['irrelevantes'] += 1
            if excluir_irrelevantes and excluir_email(service, message['id']):
                excluido = True
                stats['excluidos'] += 1

        elif classificacao == 'IMPORTANTE':
            stats['importantes'] += 1

        emails_processados.append({
            'id': message['id'],
            'remetente': remetente,
            'assunto': assunto,
            'data': data,
            'classificacao': classificacao,
            'titulo_resumido': titulo,
            'resumo': resumo,
            'excluido': excluido
        })

        if idx < len(messages):
            time.sleep(delay)

    return {
        'mensagens': emails_processados,
        'estatisticas': stats,
        'status': status_geral
    }
