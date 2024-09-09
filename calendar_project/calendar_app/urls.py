from django.urls import path
from .views import list_events, create_event, update_event, delete_event

urlpatterns = [
    path('list_events/', list_events, name='list_events'),
    path('create_event/', create_event, name='create_event'),
    path('update_event/', update_event, name='update_event'),
    path('delete_event/', delete_event, name='delete_event'),
]