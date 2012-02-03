# -*- coding: utf-8 -*-
# Create your views here.

import re
import os
from os import listdir
from os.path import join
import testhaar
import PhotoDatabase
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import forms,models


def MainPage(request):
  return render_to_response( 'main_page.html', {} )

def Galeria(request):

  photos = []
#  for photo in [ x for x in listdir( join(settings.MEDIA_ROOT, 'Uploads/')  ) if x != 'Portraits') or (x != '.directory')]:
  """
  for photo in [ x for x in listdir( join(settings.MEDIA_ROOT, 'Uploads/')  ) if x not in ('Portraits', '.directory')]:
   
    photos.append({
        'name':photo,
        'path': 'Uploads/'+ photo,
        'portraits': [{ 'name':x, 'path': '/Uploads/Portraits/'+x} for x in listdir( join(settings.MEDIA_ROOT, 'Uploads/Portraits') ) if re.match('^' + photo[:4] + '_\d.png', x) ]
          })
    """
  for photo in models.Photo.objects.all():
    portraits = []
    for portrait in models.Portrait.objects.filter( fromPhoto = photo ):
      portraits.append({
          'name': portrait.name,
          'path': portrait.path, 
          })
    photos.append({
        'name': photo.path,
        'path': photo.path,
        'portraits': portraits,
        })


  return render( request, 'WebUi/galleria.html', { 'photos':photos} )

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
    photo_name = request.FILES['file'].name
    photo_path = join( u'Uploads', request.FILES['file'].name )
    handle_uploaded_file(request.FILES['file'])    
    
    portraits = testhaar.find_faces( photo_name )
    p = models.Photo(path= photo_path)
    p.save()
    
    
    q = models.Portrait.objects.all()
    portrait_pair = []
    if q.count() > 2:#q tiene que ser mayor a 2 para que se pueda hacer una proyeccion
      print 'Encontraron Rostros'
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
    
    return render( request, 'WebUi/upload_photo.html', { 'photo_path': photo_path ,'portraits':portrait_pair, 'autocomplete_list':autocomplete_list} )
  else:
    #form = forms.PhotoForm()
    return render( request, 'WebUi/upload_photo.html', {'photo_path':'', 'portraits':'', })
  

def handle_uploaded_file(file_data):
  destination = open( join(  settings.MEDIA_ROOT, 'Uploads/') + file_data.name , 'wb+')
  
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
    path = join(settings.MEDIA_ROOT, request.POST.get('portrait_path'))
    parent_path = request.POST.get('parent_photo')
        
    portrait = PhotoDatabase.Portrait(path,name)
    parent = models.Photo.objects.get(path=parent_path)
    
    p = models.Portrait(name=name,path=request.POST.get('portrait_path'),array=portrait.vector,fromPhoto=parent)
    p.save()
    
    return HttpResponse('Portrait_Chosen')

@csrf_exempt
def Portrait_Rejected(request):
  """
  Remueve la imagen
  """
  if request.method == 'POST':
    portrait_path = request.POST.get('portrait_id')#Remueve el / inicial
    os.remove( join( settings.MEDIA_ROOT, portrait_path) )
    return HttpResponse('Portrait_Rejected Sucess')
  else:
    return HttpResponse('Portrait_Rejected Failed')
