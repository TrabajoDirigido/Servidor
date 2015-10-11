from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import ClientInfo
from ipware.ip import get_ip
import json
import socket

connected_clients = {}


# Create your views here.
def register(request):
    try:
        names = request.GET['names']
        ip = get_ip(request)

        if ip is None:
            return HttpResponse(status=500)

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
    message = {'message': message}
    message = json.dumps(message)+"\r\n"

    for ip in connected_clients:
        connected_clients[ip].send(message.encode())

    return HttpResponse(status=200)


def unregister(request):
    token = request.GET['token']

    s = connected_clients[token]
    s.send("\r\n".encode())

    try:
        client = ClientInfo.objects.get(address=token)
        client.delete()
        return HttpResponse(status=200)

    except ClientInfo.DoesNotExist:
        return HttpResponse(status=500)
