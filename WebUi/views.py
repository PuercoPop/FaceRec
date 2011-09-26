# Create your views here.

import testhaar
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
    #form = UploadFileForm(request.POST, request.FILES)
    #if form.is_valid():
    handle_uploaded_file(request.FILES['file'])    
    
    #portraits = find_face(,)
    
    return render_to_response( 'upload_photo.html', { 'photo_path':'' ,'portraits':''} )
  else:
    #form = forms.PhotoForm()
    return render_to_response( 'upload_photo.html', {'photo_path':'', 'portraits':''} )    
  


def handle_uploaded_file(file_data):
    destination = open( file_data.name, 'wb+')
    for chunk in file_data.chunks():
        destination.write(chunk)
    destination.close()
    