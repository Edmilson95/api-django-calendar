from django.shortcuts import render

# Create your views here.


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import (
    create_google_calendar_event,
    update_google_calendar_event,
)
from googleapiclient.errors import HttpError

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