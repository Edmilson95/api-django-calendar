from django.test import TestCase
from django.urls import reverse
import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

# Create your tests here.

class CalendarEventTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.token = AccessToken.for_user(self.user)

        self.client = APIClient()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

    def teste_create_event(self):
        data = {
            'email':'edmilson.svic@gmail.com',
            'summary':'Teste Automatizado',
            'start_time': '2024-10-29T15:00:00-03:00',
            'end_time': '2024-10-29T16:00:00-03:00'
        }

        response = self.client.post(reverse('create_event'), data, format='json')

        self.assertEqual(response.status_code, 201)

        self.assertIn('link', response.json())

