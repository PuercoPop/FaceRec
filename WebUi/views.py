# -*- coding: utf-8 -*-
# Create your views here.

import os,testhaar#, TestPhotoDatabase
from django.shortcuts import render_to_response
from django.http import HttpResponse
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

@csrf_exempt
def Portrait_Chosen(request):
  """
  ToDo: Introducir el Rotulo de la image, asociado al portrait y la imagen inicial mostrada
  Idea: hacer un <filename>.json para cada foto y listar los filenames y rótulos de cada
  Idea: una base de datos con photo_filename, portrait_filename y portrait_id (tal vez location in the photo coords)
  """
  return HttpResponse('Portrait_Chosen')

@csrf_exempt
def Portrait_Rejected(request):
  """
  Remueve la imagen
  """
  if request.method == 'POST':
    portrait_path = request.POST.get('portrait_id')[1:]#Remueve el / inicial
    os.remove(portrait_path)
    return HttpResponse('Portrait_Rejected Sucess')
  else:
    return HttpResponse('Portrait_Rejected Failed')