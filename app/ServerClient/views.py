from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import ClientInfo
from ipware.ip import get_ip
import socket

connected_clients = {}


# Create your views here.
def register(request):
    try:
        names = request.GET['names']
        ip = get_ip(request)

    except KeyError:
        return HttpResponse(status=500)

    try:
        ClientInfo.objects.get(address=ip)

    except ClientInfo.DoesNotExist as e:
        print(e)
        client = ClientInfo(names=names, address=ip)
        client.save()

    response = {'token': ip, 'port': 2000}
    return JsonResponse(response)


def check_connected_clients(request):
    return JsonResponse(connected_clients)


def broadcast_message(request):
    message = request.GET['message']

    for ip in connected_clients:
        connected_clients[ip].send(message.encode())

    return HttpResponse(status=200)
