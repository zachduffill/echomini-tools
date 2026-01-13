from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout


class LogWindow(QDialog):
    def __init__(self, log, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Logs")
        self.resize(900,400)

        layout = QVBoxLayout()
        logtext = "\n".join(log)

        self.textbox = QTextEdit()
        self.textbox.setReadOnly(True)
        self.textbox.setPlainText(logtext)

        btns = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_log)
        btns.addWidget(clear_button)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        btns.addWidget(close_button)

        layout.addWidget(self.textbox)
        layout.addLayout(btns)
        self.setLayout(layout)

    def clear_log(self):
        self.textbox.clear()
        self.parent().log = []
        self.parent().log_button.hide()
        self.parent().status.setText("Status")
        self.close()