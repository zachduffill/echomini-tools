import os
from pathlib import Path

from mutagen import File
from mutagen.flac import FLAC
import ffmpeg

def fix_blocksize(path, new_blocksize = 4000):
    audio = File(path)
    cls = audio.__class__.__name__
    if cls != FLAC:
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
    p = Path(path)
    tmp = p.with_suffix(".tmp.flac")

    (
        ffmpeg.input(str(p))
        .output(
            str(tmp),
            compression_level=12,
            flac_blocksize=new_blocksize,
        )
        .overwrite_output()
        .run(capture_stdout=True)
    )

    os.replace(tmp, p)

