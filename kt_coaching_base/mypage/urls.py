from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.mypage_view, name='mypage_view'),
    path('myp_info/', views.myp_info, name='myp_info'),
    path('myp_survey/', views.myp_survey, name='myp_survey'),
    path('myp_self/', views.myp_self, name='myp_self'),
    path('update_profile/', views.update_profile, name='update_profile'),
]
