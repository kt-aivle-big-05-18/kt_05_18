# community/urls.py
from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path("notice/<int:pk>/", views.notice_detail, name="notice_detail"),
    path("notice/create/", views.notice_create, name="notice_create"),
    path('survey/', views.survey_list, name="survey_list")
]