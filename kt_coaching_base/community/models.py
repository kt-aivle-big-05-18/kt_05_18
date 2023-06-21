# community/models.py
from django.db import models
import os

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="uploads/", null=True, blank=True)

    # def filename(self):
    #     return self.file.name.split("/")[-1].split("uploads/")[-1]
    def get_filename(self):
        return os.path.basename(self.file.name)
    
class Survey(models.Model):
    question = models.CharField(max_length=200)
    options = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)