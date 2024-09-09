import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

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

def get_google_calendar_events(event_id): # busca evento pelo id
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)
        
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        return event  
    except HttpError as error:
        raise Exception(f'Ocorreu um erro ao recuperar o(s) evento(s): {error}')

def list_google_calendar_events(time_min=None, time_max=None, title=None, max_results=None): #lista com base em critérios
    try:
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        params = {
            'calendarId': 'primary',
            'singleEvents': True,
            'orderBy': 'startTime',
        }

        if time_min:
            params['timeMin'] = time_min
        if time_max:
            params['timeMax'] = time_max
        if title:
            params['q'] = title

        events_result = service.events().list(**params).execute()
        events = events_result.get('items', []) 
        return events

    except HttpError as error:
        raise Exception(f'Ocorreu um erro ao listar os eventos: {error}')       


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
          
def update_google_calendar_event(event_id, event_data):
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        event = service.events().get(calendarId='primary', eventId=event_id).execute()

        # atualiza apenas os campos fornecidos
        if 'summary' in event_data:
            event['summary'] = event_data['summary']
        if 'email' in event_data:
            event['attendees'] = [{'email': event_data['email']}]
        if 'start_time' in event_data:
            event['start'] = {
                'dateTime': event_data['start_time'],
                'timeZone': 'America/Sao_Paulo',
            }
        if 'end_time' in event_data:
            event['end'] = {
                'dateTime': event_data['end_time'],
                'timeZone': 'America/Sao_Paulo',
            }

        updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        return updated_event

    except HttpError as error:
        raise Exception(f'Ocorreu um erro ao atualizar o evento: {error}')     

def delete_google_calendar_event(event_id):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    
    service.events().delete(calendarId='primary', eventId=event_id).execute()           