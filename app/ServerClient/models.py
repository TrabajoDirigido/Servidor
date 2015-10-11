from django.db import models

# Create your models here.
class ClientInfo(models.Model):
    names = models.CharField(max_length=250)
    address = models.CharField(max_length=20)

class Lab(models.Model):
    lab = models.TextField()

class Query(models.Model):
    query = models.TextField()
    lab = models.ForeignKey(Lab)