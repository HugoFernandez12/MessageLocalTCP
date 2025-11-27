from windows.userListWindow import *
from PyQt5.QtGui import *


class LoginWindow(QMainWindow):
    def __init__(self, _client, _communicator):
        super().__init__()
        self.communicator = _communicator
        self.client = _client
        self.user_list_window = None

        self.setWindowTitle("Bienvenido")
        self.setFixedSize(800, 600)

        QFontDatabase.addApplicationFont("../assets/fonts/static/Roboto-SemiBold.ttf")
        fuenteTitulo = QFont("Roboto", 20)
        fuenteSubtitulo = QFont("Roboto", 10)
        fuenteCampoUsuario = QFont("Roboto", 10)
        fuenteBoton = QFont("Roboto", 10)

        self.texto_bienvenida = QLabel("Bienvenido")
        self.texto_bienvenida.setObjectName("titulo")
        self.texto_bienvenida.setAlignment(Qt.AlignCenter)
        self.texto_bienvenida.setFont(fuenteTitulo)

        self.subtexto_bienvenida = QLabel("Introduzca un nombre de usuario para empezar a chatear")
        self.subtexto_bienvenida.setObjectName("subtitulo")
        self.subtexto_bienvenida.setAlignment(Qt.AlignCenter)
        self.subtexto_bienvenida.setFont(fuenteSubtitulo)

        self.campo_usuario = QLineEdit()
        self.campo_usuario.setObjectName("campoUsuario")
        self.campo_usuario.setMaxLength(15)
        self.campo_usuario.setAlignment(Qt.AlignCenter)
        self.campo_usuario.setFont(fuenteCampoUsuario)

        self.boton = QPushButton("Aceptar")
        self.boton.setObjectName("botonGuardarUsuario")
        self.boton.setFont(fuenteBoton)

        self.campo_usuario.returnPressed.connect(self.boton.click)
        self.boton.clicked.connect(self.sendUsername)
        self.communicator.username_response.connect(self.handleUsernameResponse)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.texto_bienvenida)
        layout.addWidget(self.subtexto_bienvenida)
        layout.addWidget(self.campo_usuario)
        layout.addWidget(self.boton)

        central_widget.setLayout(layout)
        central_widget.setObjectName("mainLayout")
        central_widget.setStyleSheet("""
            #mainLayout {
                background: #000000;
            }
            #titulo {
                color: white;
            }
            #subtitulo {
                color: white;
            }
            #campoUsuario {
                padding: 5px;
                border: 2px solid #FF8000;
                border-radius: 10px;
            }
            #botonGuardarUsuario {
                background-color: #FF8000;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 10px;
            }
            #botonGuardarUsuario:hover {
                background-color: #FF6000;
            }
        """)

    def sendUsername(self):
        username = self.campo_usuario.text().strip()
        if username:
            self.client.sendMessage(f"USER_NAME {username}")

    def handleUsernameResponse(self, is_valid):
        if is_valid:
            self.hide()
            self.user_list_window = UserListWindow(self.client, self.communicator, self.campo_usuario.text())
            self.user_list_window.show()
        else:
            QMessageBox.warning(self, "Error", "El nombre de usuario no es válido o ya está en uso.")
