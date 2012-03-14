import cv,os, numpy, PIL.Image
from django.db import models
from django.conf import settings
from django.core.files import File
from os.path import join, splitext


class Photo(models.Model):
    file = models.ImageField( upload_to= 'Uploads')

    def find_faces(self):
        cascade = cv.Load(join(settings.STATIC_ROOT,
            'other','haarcascade_frontalface_alt.xml'))
        img = cv.LoadImage( self.file.path )
        imgGray = cv.CreateImage( cv.GetSize(img), img.depth, 1)
        cv.CvtColor(img, imgGray, cv.CV_BGR2GRAY)

        faces = cv.HaarDetectObjects( imgGray, cascade, cv.CreateMemStorage(),)

        for counter , ((x, y, w, h), n) in enumerate(faces):
            cv.SetImageROI( img, (x, y, w, h) ) #Region of Interest
            imgface = cv.CreateImage( cv.GetSize(img),
                    img.depth,
                    img.nChannels
                    )
            imgface_rsz = cv.CreateImage( (64, 64), img.depth, img.nChannels )
            cv.Copy(img, imgface )
            cv.Resize( imgface, imgface_rsz, cv.CV_INTER_AREA )
            portrait_name = ''.join( [splitext(self.filename)[0],
                '_',
                str(counter),'.png']
            )
            portrait_path = join( settings.MEDIA_ROOT,
                              'Uploads',
                              'Portraits',
                              portrait_name )
            portrait_alt_path = join( settings.MEDIA_ROOT,
                              'Temp',
                              portrait_name )
            cv.SaveImage(portrait_alt_path, imgface_rsz)
            tmp_portrait = open(portrait_alt_path,'r')

            portrait_file = File(tmp_portrait)
            portrait = Portrait ( file= portrait_file,
                              fromPhoto=self )

            portrait.save()
            tmp_portrait.close()
            os.remove(portrait_alt_path)
            cv.ResetImageROI(img)

    def find_faces_no_rsz(self):
        cascade = cv.Load(join(settings.STATIC_ROOT,
            'other','haarcascade_frontalface_alt.xml')
            )
        portrait_list = []
        img = cv.LoadImage( self.file.path )
        imgGray = cv.CreateImage( cv.GetSize(img), img.depth, 1)
        cv.CvtColor(img, imgGray, cv.CV_BGR2GRAY)

        faces = cv.HaarDetectObjects( imgGray, cascade, cv.CreateMemStorage(),)

        for counter , ((x, y, w, h), n) in enumerate(faces):
            cv.SetImageROI( img, (x, y, w, h) ) #Region of Interest
            imgface = cv.CreateImage( cv.GetSize(img),
                    img.depth,
                    img.nChannels
                    )
            cv.Copy(img, imgface )
            portrait_name = ''.join( [splitext(self.filename)[0],
                '_',
                str(counter),
                '.png']
            )
            portrait_path = join( settings.MEDIA_ROOT,
                              'Uploads',
                              'Portraits',
                              portrait_name )
            cv.SaveImage(portrait_path, imgface)
            tmp_portrait = open(portrait_path,'r')
            portrait_file = File(tmp_portrait)
            portrait = Portrait ( file= portrait_file,
                              array='NULL',
                              fromPhoto=self )

            portrait_list.append( portrait )
            cv.ResetImageROI(img)

        return portrait_list

    @property
    def filename(self):
        return self.file.name.split('/')[-1]

    def delete(self):
        os.remove( self.file.path )
        super(Photo, self).delete()

    def __unicode__(self):
        return '%s' % (self.file)

class Portrait(models.Model):
    """
    guarda el nombre de la foto de la cual se retrato

    -Cuando se modifica el atributo isFace y hay mas de N Rostros se debe
    recalcular los parametros de distancia entre rostros y de distancia inter-
    rostros.
    """
    name = models.CharField(max_length=100, blank=True)
    file = models.ImageField( upload_to='Uploads/Portraits')
    #Array usar numpy.tostr method
    #array = models.CharField(max_length=200, null=True)
    fromPhoto = models.ForeignKey('Photo')
    isFace = models.NullBooleanField()
    objects = ProfileManager()

    @property
    def as_vector(self):
        return numpy.asmatrix(
                PIL.Image.open( self.file.path  )
                ).convert("L").reshape(1,-1)

    @property
    def as_difference_vector(self):
        return self.mean - self.as_vector()

    @property
    def filename(self):
        return self.file.name.split('/')[-1]

    def delete(self):
        os.remove( self.file.path )
        super(Portrait, self).delete()

    def __unicode__(self):
        return '%s is %s' % (self.file, self.name)

class ProfileManager(models.Manager):
    """
    TODO
    Cuando se da nombre se vuelve isFace true.
    Cuando se pone isFace False se borra el link al profile / nombre
    """
    def mean_vector(self):
        mean_vector = 0
        for portrait in super(ProfileManager, self.get_query_set()):
            portrait.as_vector()

        return mean_vector

class Profile(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    mean = models.FloatField()
    std_dev = models.FloatField()
    portrait_list = models.ManyToManyField('Portrait')

    def calculate_profile_parameters(self):
        """
        Calculate mean image and intra-profile distance
        """
        m_portraits = None
        for portrait in self.portrait_list:
            if m_portraits is None:
                m_portraits = numpy.copy( portrait.as_vector() )
            else:
                m_portraits = numpy.vstack(
                        (m_portraits, portrait.as_vector() )
                        )
        mean = m_portraits.mean( axis = 0 )
        #Now calculate intra-profile distance
        m_portraits -= mean
        m_portraits = m_portraits.average( axis = 0)
        #1st method
        avg_distance = 0
        for portrait in self.portrait_list:
            avg_distance += mean - portrait.as_vector
        avg_distance = avg_distance / self.portrait_list.count()


class ExtraProfileInfo(models.Model):
    inter_portrait = models.FloatField()
    intra_portrait = models.FloatField()

    def __unicode__(self):
        return u''
