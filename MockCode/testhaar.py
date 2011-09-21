import cv
import os


def find_faces():
  cascade = cv.Load('haarcascade_frontalface_alt.xml')
  
  directory = 'Images/'

  for counter_imagen , image in enumerate(os.listdir(directory)):
    img = cv.LoadImage(directory+image)
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
      cv.SaveImage("Temp_Faces/face_" +str(image[:-4])+"_"+str(counter)+".png",imgface_rsz)
      cv.ResetImageROI(img)
  
 
if __name__ == "__main__":
  find_faces()
  
