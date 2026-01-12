from PySide6.QtWidgets import (
    QHBoxLayout, QComboBox, QLineEdit, QPushButton, QFileDialog, QWidget
)

class PickerBanner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)

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
        layout.addWidget(self.picker_mode_box)
        layout.addWidget(self.picker_path)
        layout.addWidget(browse_button)

    def update_placeholder(self, mode):
        self.picker_path.setText("")
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

