from PyQt5.Qt import *


class ApplicationWindow(QMainWindow):
    def __init__(self, _client, _communicator, _target_username, my_username):
        super().__init__()
        self.client = _client
        self.communicator = _communicator
        self.target_username = _target_username
        self.my_username = my_username
        self.chat_window = None

        self.setWindowTitle(f"Solicitud de chat de {_target_username}")
        self.setFixedSize(700, 300)

        QFontDatabase.addApplicationFont("../assets/fonts/static/Roboto-SemiBold.ttf")
        fuenteTitulo = QFont("Roboto", 14)
        fuenteBoton = QFont("Roboto", 10)

        self.message_label = QLabel(f"El usuario {self.target_username}\nquiere empezar un chat contigo.", self)
        self.message_label.setObjectName("mensajePeticionChat")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFont(fuenteTitulo)

        self.accept_button = QPushButton("Aceptar", self)
        self.accept_button.setObjectName("botonAceptar")
        self.accept_button.setFont(fuenteBoton)

        self.reject_button = QPushButton("Rechazar", self)
        self.reject_button.setObjectName("botonRechazar")
        self.reject_button.setFont(fuenteBoton)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.accept_button.clicked.connect(self.onAccept)
        self.reject_button.clicked.connect(self.onReject)

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.accept_button)
        button_layout.addStretch()
        button_layout.addWidget(self.reject_button)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)
        central_widget.setObjectName("mainLayout")
        central_widget.setStyleSheet("""
            #mainLayout {
                background: #000000;
            }
            #mensajePeticionChat {
                color: white;
            }
            #botonAceptar {
                color: white;
                border-radius: 10px;
                background-color: #FF8000;
                padding: 15px;
                margin-left: 20px;
            }
            #botonAceptar:hover {
                background-color: #FF6000;
            }
            #botonRechazar {
                color: white;
                border-radius: 10px;
                background-color: #FF8000;
                padding: 15px;
                margin-right: 20px;
            }
            #botonRechazar:hover {
                background-color: #FF6000;
            }
        """)

    def onAccept(self):
        self.client.sendMessage(f"REQUEST_TRUE {self.target_username}")
        self.hide()
        self.communicator.accepted_request.emit(self.target_username)

    def onReject(self):
        self.client.sendMessage(f"REQUEST_FALSE {self.target_username}")
        self.hide()
