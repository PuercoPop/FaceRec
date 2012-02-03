# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from WebUi import views

urlpatterns = patterns('',
                       url(r'^upload_photo.html$',
                           views.UploadPhoto,
                           name="upload_photo"
                           ),

                       url(r'^gallery.html$',
                           views.Galeria,
                           name="gallery"
                           ),

                       url(r'portrait_chosen',
                           views.Portrait_Chosen,
                           name="portrait_chosen"
                           ),

                       url(r'portrait_rejected',
                           views.Portrait_Rejected,
                           name="portrait_rejected"
                           ),
)
