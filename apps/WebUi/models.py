import cv,os
from django.db import models
from django.conf import settings
from django.core.files import File
from os.path import join, splitext


# Create your models here.

class Photo(models.Model):
  file = models.ImageField( upload_to= 'Uploads')

  def find_faces(self):
    cascade = cv.Load(join(settings.STATIC_ROOT,'other','haarcascade_frontalface_alt.xml'))
    portrait_list = []
    img = cv.LoadImage( self.file.path )
    imgGray = cv.CreateImage( cv.GetSize(img), img.depth, 1)
    cv.CvtColor(img, imgGray, cv.CV_BGR2GRAY)

    faces = cv.HaarDetectObjects( imgGray, cascade, cv.CreateMemStorage(),)
    
    for counter , ((x, y, w, h), n) in enumerate(faces):
        cv.SetImageROI( img, (x,y,w,h)) #Region of Interest
        imgface = cv.CreateImage( cv.GetSize(img), img.depth, img.nChannels )
        imgface_rsz = cv.CreateImage( (64,64), img.depth, img.nChannels )
        cv.Copy(img, imgface )
        cv.Resize( imgface, imgface_rsz, cv.CV_INTER_AREA )
        portrait_name = ''.join( [splitext(self.photo_name)[0], '_', str(counter),'.png'] )
        portrait_path = join( settings.MEDIA_ROOT,
                              'Uploads',
                              'Portraits',
                              portrait_name )
        portrait_alt_path = join( settings.MEDIA_ROOT,
                              'Temp',
                              portrait_name )
        #print self.photo_name
        #print portrait_name
        print portrait_alt_path
        cv.SaveImage(portrait_alt_path, imgface_rsz)
        tmp_portrait = open(portrait_alt_path,'r')

        portrait_file = File(tmp_portrait)
        portrait = Portrait ( name= portrait_name,
                              file= portrait_file,
                              array='NULL',
                              fromPhoto=self )

        portrait.save()
        tmp_portrait.close()
        os.remove(portrait_alt_path)
        cv.ResetImageROI(img)


  
  def find_faces_no_rsz(self):
    cascade = cv.Load(join(settings.STATIC_ROOT,'other','haarcascade_frontalface_alt.xml'))
    portrait_list = []
    img = cv.LoadImage( self.file.path )
    imgGray = cv.CreateImage( cv.GetSize(img), img.depth, 1)
    cv.CvtColor(img, imgGray, cv.CV_BGR2GRAY)

    faces = cv.HaarDetectObjects( imgGray, cascade, cv.CreateMemStorage(),)
    
    for counter , ((x, y, w, h), n) in enumerate(faces):
        cv.SetImageROI( img, (x,y,w,h)) #Region of Interest
        imgface = cv.CreateImage( cv.GetSize(img), img.depth, img.nChannels )
        #imgface_rsz = cv.CreateImage( (128,128), img.depth, img.nChannels )
        cv.Copy(img, imgface )
        #cv.Resize( imgface, imgface_rsz, cv.CV_INTER_AREA )
        portrait_name = ''.join( [splitext(self.photo_name)[0], '_', str(counter),'.png'] )
        portrait_path = join( settings.MEDIA_ROOT,
                              'Uploads',
                              'Portraits',
                              portrait_name )
        cv.SaveImage(portrait_path, imgface)
        tmp_portrait = open(portrait_path,'r')
        portrait_file = File(tmp_portrait)
        portrait = Portrait ( name= portrait_name,
                              file= portrait_file,
                              array='NULL',
                              fromPhoto=self )
        portrait_list.append( portrait )
        cv.ResetImageROI(img)

    return portrait_list

  @property
  def photo_name(self):
    return self.file.name.split('/')[-1]

  def delete(self):
    os.remove( self.file.path )
    super(Photo, self).delete()

  def __unicode__(self):
    return '%s' % (self.file)

class Portrait(models.Model):
  """
  guarda el nombre de la foto de la cual se retrato
  """
  name = models.CharField(max_length=100) #min_length=1
  file = models.ImageField( upload_to='Uploads/Portraits')
  array = models.CharField(max_length=200, null=True)#Array usar numpy.tostr method
  fromPhoto = models.ForeignKey('Photo')

  def delete(self):
    os.remove( self.file.path )
    super(Portrait, self).delete()

  def __unicode__(self):
    return '%s' % (self.file)

class Profile(models.Model):
  """
  """
  name = models.CharField(max_length=20,primary_key=True)
  mean = models.FloatField()
  std_dev = models.FloatField()
  portrait_list = models.ManyToManyField('Portrait')


