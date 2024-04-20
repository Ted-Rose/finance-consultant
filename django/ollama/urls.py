from django.urls import path
from . import views

urlpatterns = [
    path('local', views.local_request, name='local_request'),
    path('production', views.production_request, name='production_request'),
    path('transcribe/', views.transcribe, name='transcribe'),
]