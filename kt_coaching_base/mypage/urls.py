from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.mypage_view, name='mypage_view'),
    path('mypage_info/', views.box_info, name='box_info'),
    path('mypage_self/', views.box_self, name='box_self'),
    path('mypage_survey/', views.box_survey, name='box_survey'),
]
