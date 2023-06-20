# rpg/urls.py
from django.urls import path, include
from .views import rpg, persona
from . import views
from analysis import views as a_views

app_name = "rpg"
urlpatterns = [
    path('rpg_start/', views.rpg, name='rpg_start'),
    path('stt/', views.stt, name="stt"),
    path('', views.persona, name='persona'),
]