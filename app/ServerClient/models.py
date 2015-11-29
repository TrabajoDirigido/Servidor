from django.db import models
import datetime

# Create your models here.
class ClientInfo(models.Model):
    names = models.CharField(max_length=250)
    address = models.CharField(max_length=20)

class Lab(models.Model):
    lab = models.TextField()
    seccion = models.TextField()
    date = models.DateField(default=str(datetime.date.today()))


class Query(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    query = models.TextField()
    lab = models.ForeignKey(Lab)
    parent= models.IntegerField()
    remaining_results = models.IntegerField()
    remaining_args = models.IntegerField()
    arg1 = models.BooleanField()

class Result(models.Model):
    value = models.TextField()
    type = models.CharField(max_length=100)
    origin = models.CharField(max_length=200,default='localhost')
    query = models.ForeignKey(Query)

class Argument(models.Model):
    value = models.TextField()
    type = models.CharField(max_length=100)
    arg1 = models.BooleanField()
    query = models.ForeignKey(Query)