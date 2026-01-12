from pathlib import Path
from echomini_tools.scripts import art, lrc, flac

def scan(root, run_flac=True, run_art=True, run_lrc=True):
    root = Path(root)

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if run_flac and path.suffix.lower() == ".flac":
            print(f"Processing FLAC: {path}")
            flac.fix(str(path))

        if run_art and path.suffix.lower() in {".mp3", ".flac", ".m4a", ".ogg"}:
            print(f"Fixing art: {path}")
            art.fix(str(path))

        if run_lrc:
            print(f"Fetching lyrics: {path}")
            lrc.get(str(path))
