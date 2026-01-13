import os
import subprocess
from pathlib import Path
from mutagen import File
from mutagen.flac import FLAC
import ffmpeg

flac_bin = None
out = print

def fix(path, _out):
    global out
    if _out is not None: out = _out

    out(f"\nFixing FLAC: {path}")

    audio = File(path)
    cls = audio.__class__.__name__
    if cls != 'FLAC':
        out(f"not a FLAC file: {path}")
        return None

    max_blocksize = audio.info.max_blocksize
    channels = audio.info.channels

    tmp = None
    if max_blocksize > 4608:
        tmp = _reduce_blocksize(path)
    if channels > 2:
        tmp = _downmix_channels(tmp or path)

    if tmp is not None:
        metadata = _extract_metadata(path)
        os.replace(tmp, path)
        _apply_metadata(path, metadata)
        out("Done")
    else:
        out(f"FLAC does not need fixing: {path}")

    return path

def _extract_metadata(path):
    audio = FLAC(path)
    tags = dict(audio.tags) if audio.tags else {}
    pictures = list(audio.pictures) if audio.pictures else []
    return tags, pictures

def _apply_metadata(path, metadata):
    audio = FLAC(path)
    tags = metadata[0]
    pictures = metadata[1]

    # tags
    audio.delete()
    for key, values in tags.items():
        for v in values:
            audio[key] = v

    # pics
    audio.clear_pictures()
    for pic in pictures:
        audio.add_picture(pic)

    audio.save()


def _downmix_channels(path):
    p = Path(path)
    tmp = p.with_suffix(".tmp.flac")

    (
        ffmpeg.input(path)
        .output(str(tmp), ac=2)
        .run()
    )

    ## Delete first tmp file if _reduce_blocksize() ran beforehand
    if str(p).endswith(".tmp.flac"): p.unlink(missing_ok=True)

    return tmp

def _reduce_blocksize(path):
    global flac_bin
    if flac_bin is None: flac_bin = _get_flac_bin()

    p = Path(path)
    tmp = p.with_suffix(".tmp.flac")

    decode = subprocess.Popen(
        [flac_bin, "-d", "--stdout", str(p)],
        stdout=subprocess.PIPE
    )
    encode = subprocess.Popen(
        [flac_bin, "--blocksize=4608", "-", "-o", str(tmp)],
        stdin=decode.stdout,
    )

    decode.stdout.close()
    encode.communicate()

    return tmp

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


