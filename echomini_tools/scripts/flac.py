import os
import subprocess
from pathlib import Path
from mutagen import File
import ffmpeg

flac_bin = None

def fix_blocksize(path):
    audio = File(path)
    cls = audio.__class__.__name__
    if cls != 'FLAC':
        print(f"Warning: '{path}' is not a FLAC file")
        return None

    max_blocksize = audio.info.max_blocksize
    channels = audio.info.channels

    _reduce_blocksize(path, max_blocksize, channels)
    return path

def _reduce_blocksize(path, blocksize, channels):
    global flac_bin
    if flac_bin is None: flac_bin = _get_flac_bin()

    args = [flac_bin]
    if blocksize > 4608: args += ["--blocksize=4608"]
    if channels > 2: args += ["--channels=2"]
    if len(args) == 1:
        print(f"File {path} does not need fixing (blocksize = {blocksize}, channels = {channels})")
        return

    p = Path(path)
    tmp = p.with_suffix(".tmp.flac")

    decode = subprocess.Popen(
        [flac_bin, "-d", "--stdout", str(p)],
        stdout=subprocess.PIPE
    )

    args += ["-", "-o", str(tmp)]
    encode = subprocess.Popen(
        args,
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


