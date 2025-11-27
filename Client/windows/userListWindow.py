from windows.applicationWindow import *
from windows.chatWindow import *


class UserListWindow(QMainWindow):
    def __init__(self, client, communicator, username):
        super().__init__()
        self.chat_window = None
        self.application_window = None
        self.client = client
        self.communicator = communicator
        self.username = username

        self.setWindowTitle("Usuarios Conectados")
        self.setFixedSize(800, 600)

        QFontDatabase.addApplicationFont("../assets/fonts/static/Roboto-SemiBold.ttf")
        fuenteUsuarioConectado = QFont("Roboto", 12)
        fuenteListadoUsuarios = QFont("Roboto", 10)

        self.label = QLabel(f"{username}")
        self.label.setObjectName("usuarioConectado")
        self.label.setFont(fuenteUsuarioConectado)
        self.label.setAlignment(Qt.AlignCenter)

        self.user_list = QListWidget()
        self.user_list.setObjectName("listadoUsuarios")
        self.user_list.setFont(fuenteListadoUsuarios)

        self.user_list.itemClicked.connect(self.select_user)
        self.communicator.update_user_list.connect(self.update_user_list)
        self.communicator.show_chat_request.connect(self.show_chat_request)
        self.communicator.start_chat.connect(self.start_chat)
        self.communicator.accepted_request.connect(self.show_chat)
        self.communicator.chat_denied.connect(self.chat_denied)
        self.communicator.show_error.connect(self.show_error)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.user_list)

        central_widget.setLayout(layout)
        central_widget.setObjectName("mainLayout")
        central_widget.setStyleSheet("""
            #mainLayout {
                background: #000000;
            }
            #usuarioConectado {
                color: white;
            }
            #listadoUsuarios {
                color: white;
                border: 2px solid #FF8000;
                border-radius: 10px;
                background-color: #000000;
            }
            #listadoUsuarios::item {
                background-color: #000000;
                color: white;
                padding: 10px;
                margin-top: 10px;
                margin-left: 30px;
                margin-right: 30px;
            }
            #listadoUsuarios::item:hover {
                background-color: #222222;
                border: 2px solid #444444;
                border-radius: 10px;
            }
        """)

    def update_user_list(self, users):
        self.user_list.clear()
        filtered = [user for user in users if user != self.username]
        for _user in filtered:
            item = QListWidgetItem(_user)
            item.setTextAlignment(Qt.AlignCenter)
            self.user_list.addItem(item)

    def show_chat_request(self, sender):
        self.application_window = ApplicationWindow(self.client, self.communicator, sender, self.username)
        self.application_window.show()

    def start_chat(self, target_username):
        self.chat_window = ChatWindow(self.client, self.communicator, target_username, self.username)
        self.chat_window.show()

    def show_chat(self, target_username):
        self.chat_window = ChatWindow(self.client, self.communicator, target_username, self.username)
        self.chat_window.show()

    @staticmethod
    def chat_denied(target_username):
        print(f"CHAT DENIED BY {target_username}")

    @staticmethod
    def show_error(message):
        print("Error:", message)

    def select_user(self, item):
        target_username = item.text()
        self.client.sendMessage(f"CHAT_REQUEST {target_username}")
