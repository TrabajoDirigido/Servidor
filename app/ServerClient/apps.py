from django.apps import AppConfig
import urllib, json, urllib.request


connected_clients = {}

class ServerClientConfig(AppConfig):
    name = 'ServerClient'
    verbose_name = "Server-Client communication"




