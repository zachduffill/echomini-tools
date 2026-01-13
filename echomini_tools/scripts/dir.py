from pathlib import Path
from echomini_tools.scripts import art, lrc, flac

def scan(root, run_art=True, run_flac=True, run_lrc=True, out=print, status=print):
    root = Path(root)

    paths = [p for p in root.rglob("*") if (p.is_file() and p.suffix.lower() in {".flac", ".m4a", ".ogg", "mp3"}) ]
    total = len(paths)

    for i in range(total):
        path = paths[i]

        if status: status(f"[{i+1}/{total}] {path.name}")
        out(f"\n[{i+1}/{total}] {path.name}")

        if run_flac and path.suffix.lower() == ".flac":
            flac.fix(str(path),_out=out)

        if run_art and path.suffix.lower() in {".mp3", ".flac", ".m4a", ".ogg"}:
            art.fix(str(path),_out=out)

        if run_lrc:
            lrc.get(str(path),_out=out)

    status("Done!")
