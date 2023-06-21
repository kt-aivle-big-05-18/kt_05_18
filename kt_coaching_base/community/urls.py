# community/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'community'
urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path("notice/<int:pk>/", views.notice_detail, name="notice_detail"),
    path("notice/create/", views.notice_create, name="notice_create"),
    path('survey/', views.survey_list, name="survey_list")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)