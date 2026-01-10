import sys
from .cli import run_cli
from .gui import run_gui

def main():
    # If arguments beyond the script name exist → CLI
    if len(sys.argv) > 1:
        return run_cli(sys.argv[1:])
    else:
        return run_gui()
