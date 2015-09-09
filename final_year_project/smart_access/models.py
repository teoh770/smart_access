from django.db import models
from django.forms import ModelForm

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    roles = models.CharField(max_length=20)
    emergencyContact = models.ForeignKey('self',null=True,blank=True)

class log(models.Model):
    user = models.ForeignKey('User', null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default="False")
