import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Necessário para acessar o Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_PATH = os.environ.get('GOOGLE_CREDENTIALS', 'credentials/credentials.json')
TOKEN_PATH = os.path.join('credentials', 'token.json')


def get_credentials():
    #Obtem as credenciais do usuario para acessar a api do google calendar
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # Se não houver credenciais válidas, o usuario precisa autenticar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para a próxima execução
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())       
    return creds  

def create_google_calendar_event(summary, start_time, end_time, email):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'attendees': [{'email': email}],
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Sao_Paulo',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }     
    return service.events().insert(calendarId='primary', body=event).execute()
          