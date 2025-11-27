class ConnectedUsers:
    def __init__(self):
        super().__init__()
        self.usuarios_conectados = {}

    def getSocketByName(self, nombre_usuario):
        for nombre, socket_cliente in self.usuarios_conectados.items():
            if nombre == nombre_usuario:
                return socket_cliente
        return None

    def getNameBySocket(self, socket_name):
        for nombre, socket_cliente in self.usuarios_conectados.items():
            if socket_cliente == socket_name:
                return nombre
        return None

    def getUsers(self):
        _usuarios = ""
        for socket_cliente, nombre in self.usuarios_conectados.items():
            _usuarios = _usuarios + " " + socket_cliente
        return _usuarios
