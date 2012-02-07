# -*- coding: utf-8 -*-
# Create your views here.

import re
import os
from os import listdir
from os.path import join

import PhotoDatabase
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

#from helpers import find_faces
import forms,models


def MainPage(request):
  return render_to_response( 'main_page.html', {} )

def Galeria(request):
  photos = models.Photo.objects.all()

  return render( request, 'WebUi/gallery.html', { 'photos':photos} )


def UploadPhoto(request):
  """
  Falta introducir el predcitor
  """
  if request.method == 'POST':
    form = forms.UploadForm( request.POST, request.FILES )
    if form.is_valid():
      photo = form.save()
      photo.find_faces()
      #for portrait in photo.objects.portraits:
      # print portrait
      return render( request, 'WebUi/upload_photo.html', {'form':form,'photo': photo } )
    
    return render( request, 'WebUi/upload_photo.html', {'form':form} )
  else:
    form = forms.UploadForm()
    return render( request, 'WebUi/upload_photo.html', {'photo_path':'', 'portraits':'', 'form': form })
  

def handle_uploaded_file(file_data):
  destination = open( join(  settings.MEDIA_ROOT, 'Uploads/') + file_data.name , 'wb+')
  
  for chunk in file_data.chunks():
    destination.write(chunk)
  destination.close()

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

def delete_photo(request):
  if request.method == 'POST':
    photo = models.Photo.objects.get(pk= request.POST.get('photo_id',None))
    for portrait in photo.portrait_set.all():
      portrait.delete()
    photo.delete()
    return redirect(request.META.get('HTTP_REFERER','upload_photo.html'))
  return HttpResponse('No POST info')
