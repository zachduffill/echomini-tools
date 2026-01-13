from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton


class LogWindow(QDialog):
    def __init__(self, log, parent=None):
        super().__init__()
        self.setWindowTitle("Logs")
        self.resize(600,400)

        layout = QVBoxLayout()

        logtext = "\n".join(log)

        self.textbox = QTextEdit()
        self.textbox.setReadOnly(True)
        self.textbox.setPlainText(logtext)
        layout.addWidget(self.textbox)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)