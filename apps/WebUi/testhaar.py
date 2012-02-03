import cv
import os
from os.path import join
from django.conf import settings


def find_faces(  img_url ):
  cascade = cv.Load( join(settings.ROOT_DIR,'apps/WebUi/haarcascade_frontalface_alt.xml') )
  directory=  join(settings.MEDIA_ROOT , 'Uploads/')
  target_directory = join( directory, 'Portraits/')
    
  portrait_list = []
  
  img = cv.LoadImage( directory + img_url)
  imgGray = cv.CreateImage( cv.GetSize(img), img.depth , 1) 
  cv.CvtColor(img, imgGray, cv.CV_BGR2GRAY)
  
  faces = cv.HaarDetectObjects( imgGray, cascade , cv.CreateMemStorage(),)

  if len(faces)>0:
    print "Detecto Algo"
  else:
    print "Miss"

  for counter , ((x, y, w, h), n) in enumerate(faces):
    cv.SetImageROI(img, (x,y,w,h ) )#Fija la region de interes
    imgface = cv.CreateImage( cv.GetSize(img),img.depth,img.nChannels)
    imgface_rsz = cv.CreateImage( (128,128) ,img.depth,img.nChannels)
    cv.Copy(img,imgface)
    cv.Resize(imgface, imgface_rsz, cv.CV_INTER_AREA)
    cv.SaveImage( target_directory + str(img_url[:-4]) + "_" + str(counter ) +".png",imgface_rsz)
    portrait_list.append( 'Uploads/Portraits/' + str(img_url[:-4]) + "_" + str(counter ) +".png")
    cv.ResetImageROI(img)
  
  return portrait_list
  
 
if __name__ == "__main__":
  find_faces_dir( '../MockUpCode/Images/')
  
  
