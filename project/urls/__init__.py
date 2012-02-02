# -*- conding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

#Apps
from WebUi.views import *

urlpatterns = patterns('',
                       url(r'WebUi/', include()),
)

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$',
                                serve, {'document_root':setttings.STATIC_ROOT, 'show_indexes': True}),
                            url(r'^media/(?P<path>.*)$',
                                serve, {'document_root':settings.MEDIA_ROOT, 'show_indexes': True}),
)
