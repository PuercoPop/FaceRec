# Create your views here.

import testhaar
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import forms as webuiforms

def MainPage(request):
  return render_to_response( 'main_page.html', {} )

@csrf_exempt
def UploadPhoto(request):
  #c = {}
  #c.update(csrf(request))
  if request.method == 'POST':
<<<<<<< Updated upstream
#    print request.FILES
#    photo_path = request.FILES['name']
#    handle_uploaded_file(request.FILES['file'], request.FILES['name'])    
=======
    print dir(request)
    print dir(request.POST)
    print dir(request.FILES)
    print request.FILES.keys()
    
    photo_path = request.FILES['name']#    handle_uploaded_file(request.FILES['file'], request.FILES['name'])    
  
>>>>>>> Stashed changes
    #portraits = find_face(,)
    
    form = webuiforms.PhotoForm(request.POST, request.FILES)
    if form.is_valid():
      handle_uploaded_file(request.FILES['photo'])
      return render_to_response( 'upload_photo.html', { 'photo_path':'' ,'portraits':'', 'ispost': True, 'uploaded_photo_ok' : True })#,c)#portraits } )
  else:
      form = webuiforms.PhotoForm()
#  return render_to_response( 'main_page.html', { 'ispost': false, 'uploaded_photo_ok' : false} )    
  return render_to_response( 'upload_photo.html', { 'photo_path':'' ,'portraits':'', 'ispost': request.method == 'POST' , 'uploaded_photo_ok' : False, 'form': form })

"""
def handle_uploaded_file(file_data,file_name):
    destination = open( file_name, 'wb+')
    for chunk in data.chunks():
        destination.write(chunk)
    destination.close()
"""

def handle_uploaded_file(f):
    destination = open('TEST_CASE1.png', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    