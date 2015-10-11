"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import threading
import socket
import ServerClient.views


def run_connection():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serversocket.bind((socket.gethostname(), 2000))

    serversocket.listen(5)
    while True:
        (clientsocket, address) = serversocket.accept()
        ip = socket.gethostbyname(address[0])
        ServerClient.views.connected_clients[ip] = clientsocket

t = threading.Thread(target=run_connection)
t.daemon = True
t.start()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lab_control/', include('LabControl.urls')),
    url(r'^server_client/', include('ServerClient.urls')),
]
