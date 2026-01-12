from PySide6.QtWidgets import QPushButton


def run_gui():
    print("Launching GUI...")

    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget,
        QVBoxLayout,
    )
    from PySide6.QtGui import Qt
    import sys
    from pathlib import Path

    from .PickerBanner import PickerBanner
    from .Tool import Tool
    from .RunBtn import RunBtn

    ICON_DIR = Path(__file__).resolve().parent / "icons"
    ART_ICON = str(ICON_DIR / "art.svg")
    LRC_ICON = str(ICON_DIR / "lrc.svg")
    FLAC_ICON = str(ICON_DIR / "flac.svg")

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("echomini-tools")
            self.resize(600, 300)

            # central
            central = QWidget()
            main_layout = QVBoxLayout(central)

            picker_banner = PickerBanner()
            art_tool = Tool("Normalise album art",
                            "Resizes and crops album art to 600x600, fix for album art not showing",
                            ART_ICON)
            flac_tool = Tool("Fix FLAC incompatibilities",
                             "Re-encodes FLAC files to make them readable by echo mini",
                             FLAC_ICON)
            lrc_tool = Tool("Fetch lyrics",
                            "Fetches lyrics from LRCLIB and saves as .lrc",
                            LRC_ICON)

            run_btn = RunBtn()

            main_layout.addWidget(picker_banner)
            main_layout.addWidget(art_tool)
            main_layout.addWidget(flac_tool)
            main_layout.addWidget(lrc_tool)
            main_layout.addWidget(run_btn)

            self.setCentralWidget(central)

    app = QApplication(sys.argv)
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    window = MainWindow()
    window.show()
    app.exec()
