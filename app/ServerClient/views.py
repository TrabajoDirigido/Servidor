from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import ClientInfo
from ipware.ip import get_ip
import json
import socket
from .utils import parse_query, get_client_side_query
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




def get_parsed_query(request):
    parsed_query = {'method': 'for',
                    'vals': {
                                'method': 'get',
                                'for': 'all',
                                'x': 2,
                                'y':3
                            },
                    'query':{
                        'method': 'compare',
                        'arg1': 'for_value',
                        'arg2':2
                    }
    }
    id = 1 #Se saca de la base de datos
    #parsed_query=json.loads(request.body.decode('utf-8'))
    parsed_query,_ = parse_query(parsed_query,id)
    #Guardar parsed_query en base de datos y luego determinar que mandar al cliente
    client_side_query = get_client_side_query(parsed_query)
    return HttpResponse(status=200)

    pass