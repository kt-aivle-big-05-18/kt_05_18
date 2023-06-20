# community/models.py
from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Survey(models.Model):
    question = models.CharField(max_length=200)
    options = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)