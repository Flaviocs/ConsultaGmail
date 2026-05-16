"""
Script para consultar emails do Gmail e listar os títulos
"""
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Escopos necessários para leitura de emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def autenticar_gmail():
    """Autentica e retorna o serviço do Gmail"""
    creds = None

    # O arquivo token.json armazena os tokens de acesso do usuário
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se não há credenciais válidas, faz login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)

            try:
                print('\n⚠️  IMPORTANTE: Não feche o navegador até completar a autorização!')
                print('   Após autorizar, aguarde o navegador ser redirecionado.\n')
                creds = flow.run_local_server(port=0)
            except AttributeError:
                print('\n❌ Erro no redirect automático.')
                print('   Vamos tentar o método manual...\n')
                creds = flow.run_console()

        # Salva as credenciais para a próxima execução
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def listar_emails(service, max_results=10):
    """Lista os emails da caixa de entrada com seus títulos"""
    try:
        # Busca os emails
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results,
            labelIds=['INBOX']
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            print('Nenhum email encontrado.')
            return

        print(f'\n📧 Listando {len(messages)} emails:\n')
        print('-' * 80)

        for idx, message in enumerate(messages, 1):
            # Obtém detalhes completos do email
            msg = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()

            headers = msg['payload']['headers']

            # Extrai informações dos headers
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sem assunto')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconhecido')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Sem data')

            print(f'{idx}. {subject}')
            print(f'   De: {from_email}')
            print(f'   Data: {date}')
            print('-' * 80)

    except HttpError as error:
        print(f'Ocorreu um erro: {error}')


def main():
    """Função principal"""
    print('🔍 Consultando Gmail...\n')

    # Autentica
    service = autenticar_gmail()

    # Lista os emails (padrão: 10 últimos)
    # Você pode alterar o número aqui
    listar_emails(service, max_results=50)


if __name__ == '__main__':
    main()
