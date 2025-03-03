from celery import shared_task
from .services import create_google_calendar_event, get_credentials
from googleapiclient.discovery import build
import datetime

@shared_task
def create_event_async(event_data):
    '''Evento assincrono'''
    creds = get_credentials()
    if not creds:
        return {"ERROR:": "Credenciais inválidas"}
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': event_data.get('summary', 'Evento Padrão'),
            'description': event_data.get('description', 'Sem descrição'),
            'start': {'dateTime': event_data.get('start_time'), 'timeZone': 'UTC'},
            'end': {'dateTime': event_data.get('end_time'), 'timeZone': 'UTC'},
            'attendees': [{'email': event_data.get('email')}],           
        }
        
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        
        return {'event_id': event_result['id'], 'status': 'success'}
    
    except Exception as e:
        return {'error': str(e)}