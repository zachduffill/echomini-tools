from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel


class RunFooter(QWidget):
    def __init__(self, on_run):
        super().__init__()

        row = QHBoxLayout()

        self.status = QLabel("Status")
        row.addWidget(self.status)

        row.addStretch()

        button = QPushButton("Run")
        button.setFixedWidth(120)
        button.clicked.connect(on_run)

        row.addWidget(button)
        self.setLayout(row)