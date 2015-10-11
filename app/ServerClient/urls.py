from ServerClient import views

from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^register/', views.register, name='register'),
                       url(r'^check_connected_clients/', views.check_connected_clients, name='check_connected_clients'),
                       url(r'^broadcast_message/', views.broadcast_message, name='broadcast_message'),
                       #url(r'^query/', views.query, name='query'),
                       #url(r'^add_lab/', views.add_lab, name='add_lab'),
                       #url(r'^results/', views.results, name='query'),
                       #url(r'^registry/', views.registry, name='registry'),
                       #url(r'^save_deleted_points_to_database/', views.save_deleted_points_to_database, name='save_deleted_points_to_database'),
                       )