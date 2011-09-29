# Create your views here.

import testhaar#, TestPhotoDatabase
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import forms

def MainPage(request):
  return render_to_response( 'main_page.html', {} )

@csrf_exempt
def UploadPhoto(request):
  if request.method == 'POST':
    photo_path = request.FILES['file'].name
    handle_uploaded_file(request.FILES['file'])    
    
    portraits = testhaar.find_faces( photo_path )
    
    return render_to_response( 'upload_photo.html', { 'photo_path':photo_path ,'portraits':portraits, 'MEDIA_URL':'Uploads/', 'STATIC_URL':'static/'} )
  else:
    #form = forms.PhotoForm()
    return render_to_response( 'upload_photo.html', {'photo_path':'', 'portraits':'', 'MEDIA_URL':'Uploads/', 'STATIC_URL':'static/'} )
  


def handle_uploaded_file(file_data):
    destination = open(  'Uploads/' + file_data.name, 'wb+')
    for chunk in file_data.chunks():
        destination.write(chunk)
    destination.close()
    