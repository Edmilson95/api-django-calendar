from django.shortcuts import render
import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import (
    list_google_calendar_events,
    get_google_calendar_events,
    create_google_calendar_event,
    update_google_calendar_event,
    delete_google_calendar_event
)
from googleapiclient.errors import HttpError

def list_events(request):
    if request.method == 'GET':
        try:
            event_id = request.GET.get('id')
            title = request.GET.get('title')
            start_date = request.GET.get('start_date')  # YYYY-MM-DD
            end_date = request.GET.get('end_date')      # YYYY-MM-DD

            if event_id:
                # Busca por ID específico
                event = get_google_calendar_events(event_id)
                event_data = {
                    'id': event.get('id'),
                    'summary': event.get('summary'),
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'attendees': event.get('attendees', [])
                }
                return JsonResponse({'event': event_data}, status=200)
            
            # se n for passado parametro, retorns os 10 prox eventos
            if not start_date and not end_date and not title:
                now = datetime.datetime.now().isoformat() + 'Z'
                events_result = list_google_calendar_events(time_min=now, max_results=10)

                events_data = []
                for event in events_result:
                    event_info = {
                        'id': event.get('id'),
                        'summary': event.get('summary'),
                        'start': event['start'].get('dateTime', event['start'].get('date')),
                        'end': event['end'].get('dateTime', event['end'].get('date')),
                        'attendees': event.get('attendees', [])
                    }
                    events_data.append(event_info)
                return JsonResponse({'events': events_data}, status=200)    

            # Busca por período de datas e título
            time_min = f"{start_date}T00:00:00Z" if start_date else None
            time_max = f"{end_date}T23:59:59Z" if end_date else None

            events = list_google_calendar_events(time_min=time_min, time_max=time_max, title=title)
            
            events_data = []
            for event in events:
                event_info = {
                    'id': event.get('id'),
                    'summary': event.get('summary'),
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'attendees': event.get('attendees', [])
                }
                events_data.append(event_info)
            
            return JsonResponse({'events': events_data}, status=200)
        
        except HttpError as error:
            return JsonResponse({'error': f'Ocorreu um erro: {error}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método inválido'}, status=400)      

@csrf_exempt
def create_event(request):
    """Cria um novo evento no Google Calendar."""
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        summary = data.get('summary')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # Validação dos dados
        if not all([email, summary, start_time, end_time]):
            return JsonResponse({'error': 'Todos os campos são obrigatórios.'}, status=400)
            
        # Criação do evento
        try:
            event = create_google_calendar_event(summary, start_time, end_time, email)
            return JsonResponse({
                'message': 'Evento criado com sucesso.',
                'link': event.get('htmlLink'),
                'event_id': event.get('id')
            }, status=201)
        
        except HttpError as error:
            return JsonResponse({'error': f'Ocorreu um erro: {error}'}, status=500)
    
    return JsonResponse({'error': 'Método inválido'}, status=400)

@csrf_exempt
def update_event(request): #atualizar evento existente
    if request.method == 'PUT':
        data = json.loads(request.body)

        event_id = data.get('id')
        event_data = {
            'email': data.get('email'),
            'summary': data.get('summary'),
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time')
        }

        if not event_id:
            return JsonResponse({'error': 'Campo ID é obrigatório.'})

        try:
            updated_event = update_google_calendar_event(event_id, {k: v for k, v in event_data.items() if v is not None})
            return JsonResponse({'message': 'Evento atualizado com sucesso.',
                                  'link': updated_event.get('htmlLink')
                                }, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    return JsonResponse({'error': 'Método inválido'}, status=400)

@csrf_exempt
def delete_event(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        event_id = data.get('id')

        if not event_id:
            return JsonResponse({'error': 'Necessário Id do evento.'}, status=400)
        
        try:
            delete_google_calendar_event(event_id)
            return JsonResponse({'message': 'Evento deletado com sucesso!'}, status=200)
        
        except Exception as e:
            return JsonResponse({'error', str(e)}, status=500)
        
    return JsonResponse({'error': 'Método de requisição inválido.'}, status=400)    