# -*- coding: utf-8 -*-

from os.path import join

from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse
from django.conf import settings

import forms, models


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
            return render(
                        request,
                        'WebUi/upload_photo.html',
                        {
                            'form':form,
                            'photo': photo
                        }
                    )

        return render(
                    request,
                    'WebUi/upload_photo.html',
                    {
                        'form':form
                    }
                )
    else:
        form = forms.UploadForm()
        return render(
                    request,
                    'WebUi/upload_photo.html',
                    {
                        'photo_path':'',
                        'portraits':'',
                        'form': form
                    }
                )

def handle_uploaded_file(file_data):
    destination = open(
                    join(
                        settings.MEDIA_ROOT,
                        'Uploads',
                        file_data.name
                    ),
                    'wb+'
                )

    for chunk in file_data.chunks():
        destination.write(chunk)
    destination.close()

def Portrait_Chosen(request):
    """
    ToDo: Introducir el Rotulo de la image, asociado al portrait y la imagen
        inicial mostrada
    Idea: hacer un <filename>.json para cada foto y listar los filenames y
        rótulos de cada
    Idea: una base de datos con photo_filename, portrait_filename y portrait_id
        (tal vez location in the photo coords) introduzco defrente el modelo a
        la DB,
    """

    if request.method == 'POST':
        name = request.POST.get('portrait_name', None)
        portrait_id = request.POST.get('portrait_id', None)
        portrait = models.Portrait.objects.get(pk = portrait_id )
        portrait.name = name
        portrait.isFace = True
        portrait.save()

        return HttpResponse('Portrait_Chosen')

    else:
        return HttpResponse('No POST INFOO')

def Portrait_Rejected(request):
    """
    Remueve la imagen
    """
    if request.method == 'POST':
        portrait_id = request.POST.get('portrait_id', None)
        portrait = models.Portrait.objects.get( pk = portrait_id )
        portrait.isFace = False
        portrait.save()
        return HttpResponse('Portrait_Rejected Sucess')
    else:
        return HttpResponse('Portrait_Rejected Failed')

def delete_photo(request):
    """
    Delete first Associated Portraits and then Photo.
    """
    if request.method == 'POST':
        photo = models.Photo.objects.get(
                    pk= request.POST.get('photo_id', None)
                )
        for portrait in photo.portrait_set.all():
            portrait.delete()
        photo.delete()
        return redirect(request.META.get('HTTP_REFERER','upload_photo.html'))
    return HttpResponse('No POST info')
