from ServerClient import views

from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^register/', views.register, name='register'),
                       url(r'^check_connected_clients/', views.check_connected_clients, name='check_connected_clients'),
                       url(r'^broadcast_message/', views.broadcast_message, name='broadcast_message'),
                       url(r'^unregister/', views.unregister, name='unregister'),
                       url(r'^get_parsed_query/', views.get_parsed_query, name='get_parsed_query'),
                       url(r'^receive_client_response/', views.receive_client_response, name='receive_client_response'),
                       url(r'^get_all_clients/', views.get_all_clients, name='get_all_clients')
                       )