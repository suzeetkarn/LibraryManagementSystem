import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Admin(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class Book(models.Model):
    uid = models.UUIDField( default = uuid.uuid4,editable = False)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=100,unique=True)
    publication = models.CharField(max_length=100)

    def __str__(self):
        return self.name









