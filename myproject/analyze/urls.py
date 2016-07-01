from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from views import *


urlpatterns = patterns('',
    url(r'^$', 'analyze.views.index'),
    url(r'^(?P<pk>\d+)/$', 'analyze.views.news'),
)
