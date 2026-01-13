from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel

from src.echomini_tools.gui.LogWindow import LogWindow


class RunFooter(QWidget):
    def __init__(self, on_run):
        super().__init__()
        self.log = []

        row = QHBoxLayout()

        self.status = QLabel("Status")
        self.status.setStyleSheet("""color: #999""")
        row.addWidget(self.status)

        row.addStretch()

        self.log_button = QPushButton("Logs")
        self.log_button.clicked.connect(self.open_log_window)
        self.log_button.hide()
        row.addWidget(self.log_button)

        run_button = QPushButton("Run")
        run_button.setFixedWidth(120)
        run_button.setStyleSheet("""background-color: #093b4f;color: white;""")
        run_button.clicked.connect(on_run)

        row.addWidget(run_button)
        self.setLayout(row)

    def open_log_window(self):
        w = LogWindow(self.log, self)
        w.exec()

    def show_log_btn(self):
        self.log_button.show()