from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CustomerDatas(models.Model):
    name=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    phnumber=models.IntegerField()
    address=models.CharField(max_length=500)
    lastcall=models.CharField(max_length=20)
    nextcall=models.CharField(max_length=20,null=True,blank=True)
    status=models.CharField(max_length=20)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')

    def __str__(self):
        return self.name
    
class Note(models.Model):
    note=models.CharField(max_length=1000,null=True,blank=True)
    user=models.ForeignKey(CustomerDatas,on_delete=models.CASCADE,related_name='noteofuser')

    def __str__(self):
        return self.note 
