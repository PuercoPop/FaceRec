from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

import WebUi.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FaceRec.views.home', name='home'),
    # url(r'^FaceRec/', include('FaceRec.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^WebUi/$',WebUi.views.MainPage ),
    url(r'^upload_photo.html$', WebUi.views.UploadPhoto),
    url(r'main_page.html',WebUi.views.MainPage),
    url(r'^Uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}), 
    
)
