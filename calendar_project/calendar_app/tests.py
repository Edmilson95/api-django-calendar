from django.test import TestCase
from django.urls import reverse
import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
import datetime

# Create your tests here.

class CalendarEventTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.token = AccessToken.for_user(self.user)

        self.client = APIClient()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        self.dados_evento = {
            'email':'edmilson.svic@gmail.com',
            'summary':'Teste Automatizado',
            'start_time': '2024-10-29T15:00:00-03:00',
            'end_time': '2024-10-29T16:00:00-03:00'
        }

        # Criar um evento para testes de update e delete
        response = self.client.post(reverse('create_event'), self.dados_evento, format='json')

        # Armazenar o ID do evento
        self.evento_id = response.json().get('event_id')

    def test_create_event(self):
        response = self.client.post(reverse('create_event'), self.dados_evento, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('link', response.json())

    def test_update_event(self):
        # Dados atualizados do evento
        dados_atualizados = {
            'summary': 'Teste Atualizado',
            'start_time': '2024-10-29T17:00:00-03:00',
            'end_time': '2024-10-29T18:00:00-03:00'
        }

        response = self.client.put(reverse('update_event'), 
            {
                'id': self.evento_id,
                **dados_atualizados
            }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Evento atualizado com sucesso.')

    def test_list_10events(self):
        response = self.client.get(reverse('list_events'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)
    
    def test_list_by_id(self):
        response = self.client.get(reverse('list_events') + f'?id={self.evento_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('event').get('id'), self.evento_id)

    def test_list_by_title(self):
        response = self.client.get(reverse('list_events') + f'?title=Teste') 
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_list_by_date(self):
        dia_de_hoje = datetime.date.today()
        response = self.client.get(reverse('list_events') + f'?start_date={dia_de_hoje}&end_date={dia_de_hoje}')
        self.assertEqual(response.status_code, 200)

    def test_delete_event_by_id(self):
        response = self.client.delete(reverse('delete_event'), {'id': self.evento_id}, format='json')
        self.assertEqual(response.status_code, 204)       