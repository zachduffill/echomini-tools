from mutagen import File
from mutagen.id3 import APIC
from mutagen.flac import Picture
from mutagen.mp4 import MP4Cover
from mutagen.oggvorbis import OggVorbis

from PIL.Image import Resampling
from io import BytesIO
from PIL import Image

def fix(path):
    pass

def load_embedded_art(source):
    if isinstance(source, str):
        audio = File(source)    # 'source' is path
    else:
        audio = source          # 'source' is object

    if audio is None: return None

    cls = audio.__class__.__name__

    match cls:
        case 'MP3' | 'ID3':
            print("File is of type MP3/ID3")
            for frame in audio.values():
                if isinstance(frame, APIC):
                    print("Found Art!")
                    return frame.mime, frame.data

            print("No Art found")
            return None
        case 'FLAC':
            print("File is of type FLAC")
            if audio.pictures:
                pic: Picture = audio.pictures[0]
                print("Found Art!")
                return pic.mime, pic.data

            print("No Art found")
            return None
        case 'MP4':
            print("File is of type M4A")
            covers = audio.get("covr")
            if covers:
                cover = covers[0]
                mime = "image/jpeg" if cover.imageformat == MP4Cover.FORMAT_JPEG else "image/png"
                print("Found Art!")
                return mime, bytes(cover)

            print("No Art found")
            return None
        case 'OggVorbis':
            print("File is of type OGG")
            if audio.pictures:
                pic = audio.pictures[0]
                print("Found Art!")
                return pic.mime, pic.data

            print("No Art found")
            return None

    print("Invalid Format")
    return None


def resize_image(data, new_size):
    img = Image.open(BytesIO(data))
    img = img.convert('RGB')

    # crop if needed, and resize
    img = _crop_to_square(img)
    img = img.resize((new_size, new_size), Resampling.LANCZOS)

    out = BytesIO()
    img.save(out, format='JPEG', quality=90)
    return out.getvalue()

def _crop_to_square(img):
    w, h = img.size
    if w != h:
        min_side = min(w, h)
        left = (w - min_side) // 2
        top = (h - min_side) // 2
        right = left + min_side
        bottom = top + min_side
        return img.crop((left, top, right, bottom))
    return img

def _get_image_size(data: bytes):
    img = Image.open(BytesIO(data))
    return img.size