import os
import subprocess
from pathlib import Path

from mutagen import File
from mutagen.flac import FLAC

flac_bin = None

def fix_blocksize(path, new_blocksize = 2048):
    audio = File(path)
    cls = audio.__class__.__name__
    if cls != 'FLAC':
        print(f"Warning: '{path}' is not a FLAC file")
        return None

    max_blocksize = audio.info.max_blocksize
    if max_blocksize is None:
        print(f"Warning: could not read blocksize for '{path}'")
        return None
    if max_blocksize < 4000:
        print(f"'{path}' blocksize is already < 4000, no changes made")
        return None

    _reduce_blocksize(path, new_blocksize)
    return path

def _reduce_blocksize(path, new_blocksize):
    global flac_bin
    if flac_bin is None: flac_bin = _get_flac_bin()

    p = Path(path)
    tmp = p.with_suffix(".tmp.flac")

    decode = subprocess.Popen(
        [flac_bin, "-d", "--stdout", str(p)],
        stdout=subprocess.PIPE
    )

    encode = subprocess.Popen(
        [flac_bin, f"--blocksize={new_blocksize}", "-", "-o", str(tmp)],
        stdin=decode.stdout,
    )

    decode.stdout.close()
    encode.communicate()

    os.replace(tmp, p)

def _get_flac_bin():
    # check /bin
    local = Path(__file__).parent / "bin" / ("flac.exe" if os.name == "nt" else "flac")
    if local.exists():
        return str(local)

    # check PATH
    from shutil import which
    path_flac = which("flac")
    if path_flac:
        return path_flac

    raise RuntimeError("Could not find flac encoder in /bin or in PATH")


