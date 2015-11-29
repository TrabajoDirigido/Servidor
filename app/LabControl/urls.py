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
                       url(r'^change_page/', views.change_page, name='change_page'),
                       url(r'^change_page_results/', views.change_page_results, name='change_page_results'),
                       url(r'^get_labs_per_seccion/' ,views.get_labs_per_seccion, name='get_labs_per_seccion'),
                       url(r'^get_table_for_lab/', views.get_table_for_lab, name='get_table_for_lab'),
                       url(r'^teacher_logout/', views.teacher_logout, name='teacher_logout'),
                       url(r'^add_Teacher/', views.add_Teacher, name='add_Teacher'),
                       )