from django.contrib import admin
from django.urls import path
from . import views #추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'), #추가
]