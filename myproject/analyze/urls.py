from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from views import index, article


urlpatterns = patterns('',
    url(r'^$', 'analyze.views.index'),
)
