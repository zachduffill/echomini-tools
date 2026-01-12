def run_gui():
    print("Launching GUI...")

    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget,
        QVBoxLayout, QHBoxLayout, QComboBox,
        QPushButton, QLineEdit, QFileDialog,
    )
    import sys

    from .PickerBanner import PickerBanner

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("echomini-tools")
            self.resize(600, 400)

            # central
            central = QWidget()
            main_layout = QVBoxLayout(central)

            picker_banner = PickerBanner()

            main_layout.addWidget(picker_banner)
            main_layout.addStretch()

            self.setCentralWidget(central)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
