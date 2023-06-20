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
    path('persona/share/<int:persona_id>/', views.share_persona, name='share_persona'),
    path('persona/stop_sharing/<int:persona_id>/', views.stop_sharing, name='stop_sharing'),
]