# rpg/urls.py
from django.urls import path, include
from . import views

app_name = "admin_page"
urlpatterns = [
    path('', views.admin_page, name='admin_page'),
]