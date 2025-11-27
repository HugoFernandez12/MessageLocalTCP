import socket
import time
import selectors
from libs.listadoUsuarios import *
from libs.bufferTcp import *

connectedUsers = ConnectedUsers()
selector = selectors.DefaultSelector()
clientTimers = {}
buff = bufferTCP(1024)


def enrouteClient(clientSocket, mask):
    try:
        message = clientSocket.recv(1024)
        if message:
            buff.addMsg(message)
            while message != "":
                message = buff.extractMsg()
                if message != "":

                    print(f"Message received: {message}")

                    if message.startswith("KEEP_ALIVE"):
                        print("KEEP_ALIVE received.")
                        clientTimers[clientSocket]["limitTime"] = time.time()

                    if message.startswith("USER_NAME"):
                        userName = message.split()[1]
                        if userName in connectedUsers.usuarios_conectados:
                            print("Usuario no valid: the user is already taken.")
                            clientSocket.send(buff.encapsulateMsg("USER_TAKEN"))
                        else:
                            clientSocket.send(buff.encapsulateMsg("USER_VALID"))
                            connectedUsers.usuarios_conectados[userName] = clientSocket
                            print(f"{userName} connected.")
                            for socket_cliente in connectedUsers.usuarios_conectados.values():
                                socket_cliente.send(buff.encapsulateMsg(f"USER_LIST{connectedUsers.getUsers()}"))

                    if message.startswith("CHAT_REQUEST"):
                        userToRequest = message.split()[1]
                        request = "CHAT_REQUEST " + connectedUsers.getNameBySocket(clientSocket)
                        connectedUsers.getSocketByName(userToRequest).send(buff.encapsulateMsg(request))

                    if message.startswith("REQUEST_TRUE"):
                        userRequestAccept = message.split()[1]
                        request = "REQUEST_ACCEPT " + connectedUsers.getNameBySocket(clientSocket)
                        connectedUsers.getSocketByName(userRequestAccept).send(buff.encapsulateMsg(request))

                    if message.startswith("REQUEST_FALSE"):
                        userRequestAccept = message.split()[1]
                        request = "REQUEST_DENIED " + connectedUsers.getNameBySocket(clientSocket)
                        connectedUsers.getSocketByName(userRequestAccept).send(buff.encapsulateMsg(request))

                    if message.startswith("CHAT_MESSAGE"):
                        userToChat = message.split()[1]
                        texto = ' '.join(message.split()[2:])
                        request = "CHAT_MESSAGE " + texto
                        connectedUsers.getSocketByName(userToChat).send(buff.encapsulateMsg(request))

        else:
            print("Client disconnected.")
            disconnectClient(clientSocket)

    except Exception as e:
        print(f"Error with a client: {e}.")
        disconnectClient(clientSocket)


def aceptar_conexion(server_socket, mask):
    clientSocket, cliente_address = server_socket.accept()
    print(f"Conexion established with {cliente_address}.")
    clientSocket.setblocking(False)

    clientTimers[clientSocket] = {
        "lastKeepAlive": time.time(),
        "limitTime": time.time()
    }

    selector.register(clientSocket, selectors.EVENT_READ, enrouteClient)


def enviar_keep_alive():
    actualTime = time.time()
    for cliente_socket in list(clientTimers.keys()):
        timers = clientTimers[cliente_socket]

        if actualTime - timers["lastKeepAlive"] >= 20:
            try:
                print(f"Sending KEEP_ALIVE to {cliente_socket.getpeername()}.")
                cliente_socket.send(buff.encapsulateMsg("KEEP_ALIVE"))
                clientTimers[cliente_socket]["lastKeepAlive"] = actualTime
            except Exception as e:
                print(f"Error sending KEEP_ALIVE: {e}.")
                disconnectClient(cliente_socket)

        if actualTime - timers["limitTime"] >= 60:
            print(f"Limit time waiting a response from {cliente_socket.getpeername()}, closing conexion.")
            disconnectClient(cliente_socket)


def disconnectClient(cliente_socket):
    if cliente_socket in clientTimers:
        del clientTimers[cliente_socket]
    for nombre, socket_cliente in list(connectedUsers.usuarios_conectados.items()):
        if socket_cliente == cliente_socket:
            del connectedUsers.usuarios_conectados[nombre]
            break
    selector.unregister(cliente_socket)
    cliente_socket.close()


def startServer(host='0.0.0.0', puerto=551):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, puerto))
    servidor_socket.listen()
    servidor_socket.setblocking(False)
    selector.register(servidor_socket, selectors.EVENT_READ, aceptar_conexion)
    print(f"Server open at {host}:{puerto}.")

    try:
        while True:
            eventos = selector.select(timeout=0.5)
            for key, mask in eventos:
                callback = key.data
                callback(key.fileobj, mask)

            enviar_keep_alive()
    except KeyboardInterrupt:
        print("Server stopped manually.")
    finally:
        selector.close()
        servidor_socket.close()


if __name__ == "__main__":
    startServer()
