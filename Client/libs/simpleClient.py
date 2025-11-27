import socket
import threading
from libs.bufferTcp import *


buff = bufferTCP(1024)


class ClientTCP:
    def __init__(self, host='127.0.0.1', puerto=12345):
        self.host = host
        self.puerto = puerto
        self.cliente_socket = None
        self.recibiendo = False
        self.callback_externo = None

    def connect(self):
        try:
            self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente_socket.connect((self.host, self.puerto))
            self.recibiendo = True
            print(f"Connected to server at {self.host}:{self.puerto}.")
            threading.Thread(target=self.receiveMessage, daemon=True).start()
        except Exception as e:
            print(f"Error connecting to the server: {e}.")

    def receiveMessage(self):
        while self.recibiendo:
            try:
                message = self.cliente_socket.recv(1024)  # .decode('utf-8')
                if message and self.callback_externo:
                    buff.addMsg(message)
                    while message != "":
                        message = buff.extractMsg()
                        if message != "":
                            self.callback_externo(message)

            except Exception as e:
                print(f"Error receiving message: {e}.")
                break

    def sendMessage(self, message: str):
        try:
            self.cliente_socket.send(buff.encapsulateMsg(message))
        except Exception as e:
            print(f"Error sending message: {e}.")

    def setCallback(self, funcion):
        self.callback_externo = funcion

    def close(self):
        self.recibiendo = False
        if self.cliente_socket:
            self.cliente_socket.close()
