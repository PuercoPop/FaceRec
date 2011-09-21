from django.db import models

# Create your models here.

class UploadImage(models.Model):
  photo = models.ImageField(upload_to='Photos/')
  
class Photo(models.Model):
  name = models.CharField(max_length=20)#min_length=1
  image = models.ImageField(upload_to='Photos/')

class Portrait(models.Model):
  """
  guarda el nombre de la foto de la cual se retrato
  """
  parent = models.CharField(max_length=20) #min_length=1
  is_portrait = models.BooleanField()
  name = models.CharField(max_length=20) #min_length=1
  image = models.ImageField(upload_to='Portrait/')
