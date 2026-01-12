
def run_gui():
    print("Launching GUI...")

    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget,
        QVBoxLayout, QHBoxLayout, QComboBox,
        QPushButton, QLineEdit, QFileDialog,
    )
    import sys

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("echomini-tools")
            self.resize(600, 400)

            # central
            central = QWidget()
            main_layout = QVBoxLayout(central)

            # filepick banner
            banner = QHBoxLayout()

            # mode dropdown
            self.picker_mode_box = QComboBox()
            self.picker_mode_box.addItems(["Song File","Music Folder"])
            self.picker_mode_box.currentTextChanged.connect(self.update_placeholder)

            # path
            self.picker_path = QLineEdit()
            self.picker_path.setPlaceholderText("Select a song file...")

            # Browse button
            browse_button = QPushButton("Browse…")
            browse_button.clicked.connect(self.select_file_or_dir)

            #######
            banner.addWidget(self.picker_mode_box)
            banner.addWidget(self.picker_path)
            banner.addWidget(browse_button)

            main_layout.addLayout(banner)
            main_layout.addStretch()

            self.setCentralWidget(central)

        def update_placeholder(self, mode):
            if mode == "Song File":
                self.picker_path.setPlaceholderText("Select a song file...")
            elif mode == "Music Folder":
                self.picker_path.setPlaceholderText("Select a folder of songs...")

        def select_file_or_dir(self):
            mode = self.picker_mode_box.currentText()

            if mode == "Song File":
                path, _ = QFileDialog.getOpenFileName(
                    self,
                    "Select Song File",
                    "",
                    "Audio Files (*.flac *.mp3 *.m4a *.ogg);;All Files (*)",
                )
                if path:
                    self.picker_path.setText(path)

            elif mode == "Music Folder":
                folder = QFileDialog.getExistingDirectory(
                    self,
                    "Select Music Folder",
                    ""
                )
                if folder:
                    self.picker_path.setText(folder)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
