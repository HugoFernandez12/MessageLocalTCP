import time

from libs.simpleClient import *
from windows.loginWindow import *


class Communicator(QObject):
    # LOGIN WINDOW
    username_response = pyqtSignal(bool)

    # USER LIST WINDOW
    update_user_list = pyqtSignal(list)
    show_chat_request = pyqtSignal(str)
    start_chat = pyqtSignal(str)
    accepted_request = pyqtSignal(str)
    chat_denied = pyqtSignal(str)
    show_error = pyqtSignal(str)

    # CHAT WINDOW
    receive_message = pyqtSignal(str)


def receiveMessage(mensaje):
    print(f"Message from server: {mensaje}")

    if mensaje.startswith("USER_VALID"):
        print("User valid")
        communicator.username_response.emit(True)

    if mensaje.startswith("USER_TAKEN"):
        print("User taken")
        communicator.username_response.emit(False)

    if mensaje.startswith("USER_LIST"):
        print(f"List of clients: {mensaje.split()[1:]}")
        time.sleep(0.3)
        communicator.update_user_list.emit(mensaje.split()[1:])

    if mensaje.startswith("CHAT_REQUEST"):
        userRequesting = mensaje.split()[1:][0]
        print(f"Chat request from {userRequesting}")
        communicator.show_chat_request.emit(userRequesting)

    if mensaje.startswith("REQUEST_ACCEPT"):
        userRequesting = mensaje.split()[1:][0]
        print(f"Request accepted from {userRequesting}")
        communicator.start_chat.emit(userRequesting)

    if mensaje.startswith("REQUEST_DENIED"):
        userRequesting = mensaje.split()[1:][0]
        print(f"Request denied from {userRequesting}")
        communicator.chat_denied.emit(userRequesting)

    if mensaje.startswith("CHAT_MESSAGE"):
        print(f"Message received from server {mensaje}")
        texto = ' '.join(mensaje.split()[1:])
        communicator.receive_message.emit(texto)

    if mensaje.startswith("KEEP_ALIVE"):
        print("received keep alive")
        client.sendMessage("KEEP_ALIVE")


if __name__ == "__main__":
    app = QApplication([])

    client = ClientTCP(host="127.0.0.1", puerto=551)
    client.connect()
    client.setCallback(receiveMessage)

    communicator = Communicator()

    loginWindow = LoginWindow(client, communicator)
    loginWindow.show()
    app.exec_()
