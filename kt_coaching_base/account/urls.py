# account/urls.py
from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check_duplicate/', views.check_duplicate, name='check_duplicate'),
    path('check_duplicate_email/', views.check_duplicate_email, name='check_duplicate_email'),
    path('check_nickname/', views.check_nickname, name='check_nickname'),
]