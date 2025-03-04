from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes', views.get_notes, name='notes'),
    path('history', views.get_history, name='history'),
]