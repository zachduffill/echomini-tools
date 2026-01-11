def run_gui():
    print("Launching GUI...")

    # Import Qt lazily so CLI mode doesn't require Qt installed
    from PySide6.QtWidgets import QApplication, QMainWindow
    import sys

    class App(QApplication):
        def __init__(self):
            super().__init__(sys.argv)

            # Create the main window
            self.window = QMainWindow()
            self.window.setWindowTitle("echomini-tools")
            self.window.resize(600, 400)
            self.window.show()

    app = App()
    app.exec()
