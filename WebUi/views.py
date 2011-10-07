# -*- coding: utf-8 -*-
# Create your views here.

import os
import testhaar
import PhotoDatabase
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import forms,models
from flag import __server__

def MainPage(request):
  return render_to_response( 'main_page.html', {} )

@csrf_exempt
def InitMethod(request):
  """
  Load Instante of db.
  """
  return HttpResponse('Portrait_Chosen')
  
@csrf_exempt
def UploadPhoto(request):
  """
  Falta introducir el predcitor
  """
  if request.method == 'POST':
    photo_path = request.FILES['file'].name
    photo_path = photo_path
    handle_uploaded_file(request.FILES['file'])    
    
    portraits = testhaar.find_faces( photo_path )
    p = models.Photo(path=u'Uploads/' + photo_path)
    p.save()
    
    
    q = models.Portrait.objects.all()
    portrait_pair = []
    if q.count() > 2:#q tiene que ser mayor a 2 para que se pueda hacer una proyeccion
      db = PhotoDatabase.PhotoDatabase()
      db.process_db()
      
      for portrait_path in portraits:
        p = db.evaluate_new_face( PhotoDatabase.Portrait(portrait_path,'blah').vectorize() )
        if p:
          portrait_pair.append( {'src':portrait_path,'name':p.name} )
        else:
          portrait_pair.append( {'src':portrait_path,'name':''} )
      
    else:
      for portrait_path in portraits:
        portrait_pair.append( {'src':portrait_path,'name':''} )
    
    fPass = True
    autocomplete_list = u'['
    for p in q.values('name').distinct('name'):
      if fPass:
        autocomplete_list += u'"' + p['name'] + u'"'
        fPass = False
      else:
        autocomplete_list += u',"'+p['name'] + u'"'
    autocomplete_list += u']'
    
    return render_to_response( 'upload_photo.html', { 'photo_path':photo_path ,'portraits':portrait_pair, 'MEDIA_URL':'Uploads/', 'STATIC_URL':'static/' , 'autocomplete_list':autocomplete_list} )
  else:
    #form = forms.PhotoForm()
    return render_to_response( 'upload_photo.html', {'photo_path':'', 'portraits':'', 'MEDIA_URL':'Uploads/', 'STATIC_URL':'static/'} )
  


def handle_uploaded_file(file_data):
    if __server__ == "home":
      destination = open(  'Uploads/' + file_data.name, 'wb+')
    elif __server__ == "production":
      destination = open(  '/home/puercopop/webapps/django/myproject/Uploads/' + file_data.name, 'wb+')
      
      
    for chunk in file_data.chunks():
        destination.write(chunk)
    destination.close()

@csrf_exempt
def Portrait_Chosen(request):
  """
  ToDo: Introducir el Rotulo de la image, asociado al portrait y la imagen inicial mostrada
  Idea: hacer un <filename>.json para cada foto y listar los filenames y rótulos de cada
  Idea: una base de datos con photo_filename, portrait_filename y portrait_id (tal vez location in the photo coords)
  introduzco defrente el modelo a la DB, 
  """
  
  if request.method == 'POST':
    name = request.POST.get('portrait_name')
    path = request.POST.get('portrait_path')[1:]
    src = request.POST.get('parent_photo')
    #src = src.replace('//','/')
    
    portrait = PhotoDatabase.Portrait(path,name)
    parent = models.Photo.objects.get(path=src)
    
    p = models.Portrait(name=name,path=path,array=portrait.vector,fromPhoto=parent)
    p.save()
    
    return HttpResponse('Portrait_Chosen')

@csrf_exempt
def Portrait_Rejected(request):
  """
  Remueve la imagen
  """
  if request.method == 'POST':
    portrait_path = request.POST.get('portrait_id')#Remueve el / inicial
    if __server__ == "home":
      os.remove(portrait_path)
    elif __server__ == "production":
      os.remove(portrait_path)
    return HttpResponse('Portrait_Rejected Sucess')
  else:
    return HttpResponse('Portrait_Rejected Failed')