from django.db import models
from account.models import Account
 
class Persona(models.Model):
    department    = models.CharField(max_length=45)
    rank          = models.CharField(max_length=45)
    age           = models.IntegerField()
    gender        = models.CharField(max_length=4)
    voice         = models.CharField(max_length=45)
    career        = models.IntegerField()
    nickname      = models.ForeignKey(Account, to_field="nickname", on_delete=models.CASCADE)

class Message(models.Model):
    name        = models.CharField(max_length=45)
    persona     = models.ForeignKey(Persona, on_delete=models.CASCADE)
    content     = models.TextField()
    send_date   = models.DateTimeField(auto_now_add=True)
    voice_url   = models.TextField()

    class Meta:
        ordering    =   ("send_date",)