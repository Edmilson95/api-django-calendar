from django.urls import path
from .views import create_event, update_event

urlpatterns = [
    path('create_event/', create_event, name='create_event'),
    path('update_event/', update_event, name='update_event'),
]