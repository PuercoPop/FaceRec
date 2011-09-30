from django.db import models

# Create your models here.

class UploadImage(models.Model):
  photo = models.ImageField(upload_to='Photos/')
  
class Photo(models.Model):
  name = models.CharField(max_length=20)
  photo_path = models.CharField(max_length=60)

class Portrait(models.Model):
  """
  guarda el nombre de la foto de la cual se retrato
  """
  name = models.CharField(max_length=20) #min_length=1
  portrait_path = models.CharField(max_length=60)
  array = models.CharField(max_length=200)#Array usar numpy.tostr method
  fromPhoto = models.ForeignKey('Photo')

class Profile(models.Model):
  """
  """
  mean = models.FloatField()
  std_dev = models.FloatField()
  portrait_list = models.ManyToManyField('Portrait')