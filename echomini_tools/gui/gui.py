from ..scripts.dir import scan

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
    from .RunFooter import RunFooter

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

            self.picker_banner = PickerBanner()
            self.art_tool = Tool("Normalise album art",
                            "Resizes and crops album art to 600x600, fix for album art not showing",
                            ART_ICON)
            self.flac_tool = Tool("Fix FLAC incompatibilities",
                             "Re-encodes FLAC files to make them readable by echo mini",
                             FLAC_ICON)
            self.lrc_tool = Tool("Fetch lyrics",
                            "Fetches lyrics from LRCLIB and saves as .lrc",
                            LRC_ICON)

            self.run_btn = RunFooter(self.onclick_run_btn)

            main_layout.addWidget(self.picker_banner)
            main_layout.addWidget(self.art_tool)
            main_layout.addWidget(self.flac_tool)
            main_layout.addWidget(self.lrc_tool)
            main_layout.addSpacing(20)
            main_layout.addWidget(self.run_btn)

            self.setCentralWidget(central)

        def onclick_run_btn(self):
            picker_path = self.picker_banner.picker_path.text()
            path = Path(picker_path)
            if (not path.is_file() and not path.is_dir()) or picker_path.strip() == "":
                self.run_btn.status.setText("Invalid filepath!")
                return None

            run_art = self.art_tool.is_checked()
            run_flac = self.flac_tool.is_checked()
            run_lrc = self.lrc_tool.is_checked()

            if run_art or run_flac or run_lrc:
                self.run_btn.status.setText("Running...")
                scan(path, run_art, run_flac, run_lrc)
                return True
            else:
                self.run_btn.status.setText("No tools selected")
                return False

    app = QApplication(sys.argv)
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    window = MainWindow()
    window.show()
    app.exec()
