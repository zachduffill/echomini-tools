import sys
from .cli import run_cli
from echomini_tools.gui.gui import run_gui

def main():
    if len(sys.argv) > 1:
        return run_cli(sys.argv[1:])
    else:
        return run_gui()
    
if __name__ == "__main__": main()

# app to help with snowsky echo mini:
    # normalise album art y
    # lrcget y
    # flac block sizes y
    # handles sync with local files