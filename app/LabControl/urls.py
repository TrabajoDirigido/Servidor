__author__ = 'Camila Alvarez'
from LabControl import views

from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^home/', views.home, name='home'),
                       url(r'^query/', views.query, name='query'),
                       url(r'^add_lab/', views.add_lab, name='add_lab'),
                       url(r'^results/', views.results, name='query'),
                       url(r'^registry/', views.registry, name='registry'),
                       )