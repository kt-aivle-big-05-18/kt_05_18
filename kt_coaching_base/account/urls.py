# account/urls.py
from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check_duplicate/', views.check_duplicate, name='check_duplicate'),
]