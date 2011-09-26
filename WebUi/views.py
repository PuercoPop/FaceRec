# Create your views here.

import testhaar
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

def MainPage(request):
  return render_to_response( 'main_page.html', {} )

@csrf_exempt
def UploadPhoto(request):
  if request.method == 'POST':
    print request.FILES
    photo_path = request.FILES['name']#    handle_uploaded_file(request.FILES['file'], request.FILES['name'])    
  
    #portraits = find_face(,)
    
    return render_to_response( 'upload_photo.html', { 'photo_path':'' ,'portraits':'',})#portraits } )
  else:
      form = webuiforms.PhotoForm()
  return render_to_response( 'main_page.html', { 'ispost': false, 'uploaded_photo_ok' : false} )    
  


def handle_uploaded_file(file_data,file_name):
    destination = open( file_name, 'wb+')
    for chunk in data.chunks():
        destination.write(chunk)
    destination.close()
    