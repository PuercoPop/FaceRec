from django.db import models

# Create your models here.

class Photo(models.Model):
  path = models.CharField(max_length=60,primary_key=True)

class Portrait(models.Model):
  """
  guarda el nombre de la foto de la cual se retrato
  """
  name = models.CharField(max_length=20) #min_length=1
  path = models.CharField(max_length=60,primary_key=True)
  array = models.CharField(max_length=200)#Array usar numpy.tostr method
  fromPhoto = models.ForeignKey('Photo')

class Profile(models.Model):
  """
  """
  name = models.CharField(max_length=20,primary_key=True)
  mean = models.FloatField()
  std_dev = models.FloatField()
  portrait_list = models.ManyToManyField('Portrait')