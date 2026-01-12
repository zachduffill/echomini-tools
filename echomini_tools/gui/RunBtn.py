from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton


class RunBtn(QWidget):
    def __init__(self):
        super().__init__()

        row = QHBoxLayout()
        row.addStretch()
        button = QPushButton("Run")
        button.setFixedWidth(120)
        row.addWidget(button)
        self.setLayout(row)