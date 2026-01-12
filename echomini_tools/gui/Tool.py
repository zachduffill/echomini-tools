from PySide6.QtWidgets import (
    QWidget, QLabel, QCheckBox,
    QHBoxLayout, QVBoxLayout
)
from PySide6.QtSvgWidgets import QSvgWidget


class Tool(QWidget):
    def __init__(self, title, desc, icon_path, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # icon
        icon = QSvgWidget(icon_path)
        icon.setFixedSize(40,40)
        layout.addWidget(icon)

        # text
        text = QVBoxLayout()
        text.setSpacing(2)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")

        desc_label = QLabel(desc)
        desc_label.setStyleSheet("color: #999;")

        text.addWidget(title_label)
        text.addWidget(desc_label)

        layout.addLayout(text)
        layout.addStretch()
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True)
        self.checkbox.setStyleSheet(""" QCheckBox::indicator { width: 30px; height: 30px; } """)
        layout.addWidget(self.checkbox)

    def is_checked(self):
        return self.checkbox.isChecked()

    def set_checked(self, value: bool):
        self.checkbox.setChecked(value)
