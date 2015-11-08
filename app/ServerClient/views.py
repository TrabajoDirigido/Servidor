from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import ClientInfo, Lab
from ipware.ip import get_ip
import json
import copy
import socket
from .database_utils import save_parsed_query_to_database, save_result
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
    parsed_query = {"id":8,
                    "method":"logic",
                    "type":"and",
                    "vals":{"id":5,
                            "method":"compare",
                            "arg1":{"id":1,
                                    "method":"get",
                                    "x":[{"var":"4","type":"int"},{"var":"4","type":"int"},
                                         {"var":"4","type":"int"},{"var":"4","type":"int"}],
                                    "y":[{"var":"1","type":"int"},{"var":"2","type":"int"},
                                         {"var":"3","type":"int"},{"var":"4","type":"int"}]
                                    },
                            "arg2":{"id":2,
                                    "method":"sort",
                                    "des":{"var":"false","type":"boolean"},
                                    "vals":{"id":1,"method":"get",
                                            "x":[{"var":"4","type":"int"},{"var":"4","type":"int"},
                                                 {"var":"4","type":"int"},{"var":"4","type":"int"}],
                                            "y":[{"var":"1","type":"int"},{"var":"2","type":"int"},
                                                 {"var":"3","type":"int"},{"var":"4","type":"int"}]
                                            }
                                    }
                            }
                    }

    id = 1#Se saca de la base de datos
    my_connected_clients={'0.0.0.0':'ble'}

    #parsed_query=json.loads(request.body.decode('utf-8'))
    #my_connected_clients = copy.deepcopy(connected_clients)

    parsed_query,_ = parse_query(parsed_query,id, my_connected_clients)

    #Guardar parsed_query en base de datos y luego determinar que mandar al cliente
    save_parsed_query_to_database(parsed_query,my_connected_clients)

    client_side_query = get_client_side_query(parsed_query,my_connected_clients)

    for c in client_side_query:
        message = json.dumps(client_side_query[c])+"\r\n"
        connected_clients[c].send(message.encode())

    return HttpResponse(status=200)


def receive_client_response(request):
    #cargo json
    response=json.loads(request.body.decode('UTF-8'))
    id_query = response['id']
    result = response['result']

    save_result(id_query, result)
    pass