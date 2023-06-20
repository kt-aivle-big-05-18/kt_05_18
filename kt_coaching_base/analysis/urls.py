from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from . import views


app_name = "analysis"
urlpatterns = [
    path("", views.analysis, name="analysis"),
    path("test/", views.test, name="test"),
]