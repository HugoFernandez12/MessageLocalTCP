from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class ChatWindow(QMainWindow):
    def __init__(self, _client, _communicator, _target_username, my_username):
        super().__init__()
        self.client = _client
        self.communicator = _communicator
        self.target_username = _target_username
        self.my_username = my_username

        self.setWindowTitle(f"Chat con {_target_username}")
        self.setFixedSize(800, 1000)

        QFontDatabase.addApplicationFont("assets/fonts/static/Roboto-SemiBold.ttf")
        fuentePersonToChat = QFont("Roboto", 14)

        self.personToChat = QLabel(f"{_target_username}")
        self.personToChat.setObjectName("personChat")
        self.personToChat.setAlignment(Qt.AlignCenter)
        self.personToChat.setFont(fuentePersonToChat)

        self.chat_display = QListWidget()
        self.chat_display.setObjectName("chatDisplay")
        self.chat_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.message_input = QLineEdit()
        self.message_input.setObjectName("messageInput")

        self.send_button = QPushButton("Enviar")
        self.send_button.setObjectName("sendButton")

        self.send_button.clicked.connect(self.send_message)
        self.communicator.receive_message.connect(self.append_message)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.personToChat)
        layout.addWidget(self.chat_display)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.message_input, stretch=4)
        button_layout.addStretch()
        button_layout.addWidget(self.send_button, stretch=1)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)
        central_widget.setObjectName("mainLayout")
        central_widget.setStyleSheet("""
            #mainLayout {
                background: #000000;
            }
            #personChat {
                color: white;
            }
            #chatDisplay {
                background-color: #000000;
                border: none;
                color: white;
            }
            #messageInput {
                color: white;
                border-radius: 10px;
                background-color: #FF8000;
                padding: 10px;
                margin-right: 0px;
            }
            #sendButton {
                color: white;
                border-radius: 10px;
                background-color: #FF8000;
                padding: 10px;
            }
            #sendButton:hover {
                background-color: #FF6000;
            }
        """)

    def append_message(self, message):
        message_widget = QWidget()
        message_widget.setStyleSheet("""
            background-color: #FF6000;
            border-radius: 10px;
            padding: 2px;
            margin-right: 80px;
            color: white;
            margin-top: 5px;
        """)

        message_label = QLabel(self.formatText(message, 30))
        message_label.setAlignment(Qt.AlignLeft)
        message_label.setStyleSheet("""
            color: white;
            font-size: 14px;
            word-wrap: break-word;
        """)
        message_label.setWordWrap(True)

        layout = QHBoxLayout()
        layout.addWidget(message_label)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setAlignment(Qt.AlignLeft)
        message_widget.setLayout(layout)

        item = QListWidgetItem()
        self.chat_display.addItem(item)
        self.chat_display.setItemWidget(item, message_widget)

        item.setSizeHint(message_widget.sizeHint())

        self.chat_display.scrollToItem(item)

    def send_message(self):
        msg = self.message_input.text().strip()
        if msg:
            self.client.sendMessage(f"CHAT_MESSAGE {self.target_username} {msg}")

            message_widget = QWidget()
            message_widget.setStyleSheet("""
                background-color: #FF8000;
                border-radius: 10px;
                padding: 2px;
                margin-left: 80px;
                color: white;
                margin-top: 5px;
            """)

            message_label = QLabel(self.formatText(msg, 30))
            message_label.setAlignment(Qt.AlignLeft)
            message_label.setStyleSheet("""
                color: white;
                font-size: 14px;
                word-wrap: break-word;
            """)
            message_label.setWordWrap(True)

            layout = QHBoxLayout()
            layout.addWidget(message_label)
            layout.setContentsMargins(10, 5, 10, 5)
            layout.setAlignment(Qt.AlignLeft)
            message_widget.setLayout(layout)

            item = QListWidgetItem()
            item.setSizeHint(message_widget.sizeHint())
            self.chat_display.addItem(item)
            self.chat_display.setItemWidget(item, message_widget)

            item.setSizeHint(message_widget.sizeHint())

            self.chat_display.scrollToItem(item)

            self.message_input.clear()

    @staticmethod
    def formatText(message, maxLengthLine):
        text = message.split()
        lengthText = 0
        textFinal = ""

        for palabra in text:
            if lengthText + len(palabra) + (1 if lengthText > 0 else 0) > maxLengthLine:
                textFinal = textFinal.strip() + '\n'
                lengthText = 0

            if len(palabra) > maxLengthLine:
                while len(palabra) > maxLengthLine:
                    textFinal += palabra[:maxLengthLine - 1] + "-\n"
                    palabra = palabra[maxLengthLine - 1:]
                textFinal += palabra + " "
                lengthText = len(palabra) + 1
            else:
                textFinal += palabra + " "
                lengthText += len(palabra) + 1

        return textFinal.strip()
