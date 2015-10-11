__author__ = 'Camila Alvarez'
import socket
import ServerClient.views


def run_connection():
    global connected_clients
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serversocket.bind((socket.gethostname(), 2000))

    serversocket.listen(5)
    while True:
        print(connected_clients)
        (clientsocket, address) = serversocket.accept()
        connected_clients[address] = clientsocket