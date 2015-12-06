from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import ClientInfo, Lab, Query
from LabControl import views
from ipware.ip import get_ip
import json
import copy
import socket
from .database_utils import save_parsed_query_to_database, save_result
from .utils import parse_query
from .client_side_utils import get_client_side_query
from django.views.decorators.csrf import csrf_exempt
import logging
connected_clients = {}

logger = logging.getLogger('error')

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
    lab = request.GET['lab']
    name = request.GET['name']
    parsed_query = json.loads(request.GET['query'])
    print(parsed_query)
    print(lab)
    print(name)
    try:
         max_query_id = Query.objects.all().order_by("-id")[0] #Se saca de la base de datos
         id = max_query_id.id+1
    except IndexError:
         id=1

    my_connected_clients={'0.0.0.0':'ble'}
    #my_connected_clients = connected_clients

    parsed_query,_ = parse_query(parsed_query,id, my_connected_clients)
    print(parsed_query)

    save_parsed_query_to_database(parsed_query,my_connected_clients,lab)

    client_side_query = get_client_side_query(parsed_query,my_connected_clients)
    print(client_side_query)
    # for c in client_side_query:
    #     for m in client_side_query[c]:
    #         message = json.dumps(m)+"\r\n"
    #         connected_clients[c].send(message.encode())
    #
    return views.query(request)

@csrf_exempt
def receive_client_response(request):
    #cargo json
    response = json.loads(request.body.decode('UTF-8'))
    origin = response['origin'] #ip del cliente

    if origin not in connected_clients:
        logger.log('Not a valid client')
        return HttpResponse(status=401)

    id_query = response['id']
    result = response['result']

    save_result(id_query, result,origin)

    for e in Query.objects.get(id=1).results.all():
        print('result:'+str(e.value))

    return HttpResponse(status=200)

