import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QMovie, QIcon
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QCoreApplication


class AssistantUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistente de Voz")
        self.setWindowIcon(QIcon("app_icon.png"))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0,0,0,180); border-radius: 15px;")

        self.setup_ui()
        self.hide()

        self.hide_timer = QTimer(self)
        self.hide_timer.timeout.connect(self.hide)

        self.position_window_bottom_right()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.icon_label = QLabel(self)
        pixmap = QPixmap("app_icon.png")
        if not pixmap.isNull():
            self.icon_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.icon_label.setFixedSize(70, 70)  # Um pouco maior que o ícone para ter borda
            self.icon_label.setStyleSheet("""
                            QLabel {
                                background-color: #FFA500; /* Cor do fundo do seu ícone na imagem (laranja/amarelo) */
                                border-radius: 35px; /* Metade do fixedSize para um círculo perfeito */
                                border: 2px solid white; /* Opcional: borda branca como na sua imagem */
                            }
                        """)
            self.icon_label.setAlignment(Qt.AlignCenter)

        else:
            print("AVISO: Imagem 'app_icon.png' não encontrada.")
            self.icon_label.setText("🎙️")
            self.icon_label.setStyleSheet("font-size: 40px; color: white;")

        header_layout.addWidget(self.icon_label)

        self.status_label = QLabel("Aguardando comando...", self)
        self.status_label.setStyleSheet("font-size: 20px; color: white; font-weight: bold;")
        self.status_label.setWordWrap(True)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.status_label.setMinimumWidth(200)


        header_layout.addWidget(self.status_label)

        main_layout.addLayout(header_layout)

        self.command_label = QLabel("", self)
        self.command_label.setStyleSheet("font-size: 16px; color: #ADD8E6; margin-top: 10px;")
        self.command_label.setWordWrap(True)
        self.command_label.hide()
        main_layout.addWidget(self.command_label)

        self.setLayout(main_layout)

    def position_window_bottom_right(self, margin=50):
        screen_geometry = QApplication.desktop().screenGeometry()

        self.adjustSize()

        x = screen_geometry.width() - self.width() - margin
        y = screen_geometry.height() - self.height() - margin

        self.move(x, y)

    def update_status_message(self, message):
        self.status_label.setText(message)
        self.command_label.hide()
        self.command_label.setText("")
        self.adjustSize()
        self.show()
        self.hide_timer.stop()

    def show_command_and_status(self, status_message, command_text):
        self.status_label.setText(status_message)
        if command_text:
            self.command_label.setText(f"Comando: {command_text}")
            self.command_label.show()
        else:
            self.command_label.hide()
            self.command_label.setText("")
        self.adjustSize()
        self.show()
        self.hide_timer.stop()

    def show_final_result(self, message, result_text):
        self.status_label.setText(message)
        if result_text:
            self.command_label.setText(f"Saída: {result_text[:200]}...")
            self.command_label.show()
        else:
            self.command_label.hide()
            self.command_label.setText("")
        self.adjustSize()
        self.show()
        self.hide_timer.start(3000)

    def hide_window(self):
        self.hide()
        self.hide_timer.stop()