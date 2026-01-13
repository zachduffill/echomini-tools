from mutagen import File
from mutagen.id3 import APIC
from mutagen.flac import Picture
from mutagen.mp4 import MP4Cover

from PIL.Image import Resampling
from io import BytesIO
from PIL import Image
import base64

out = print

def fix(path, new_size=600, _out=None):
    global out
    if _out is not None: out = _out

    out(f"\nFixing art: {path}")

    audio = File(path)
    cls = audio.__class__.__name__
    if audio is None or cls == "NoneType":
        return False

    art_mime, art_data = load_embedded_art(audio)
    if art_data is False:
        out(f"Invalid Format {cls}: {path}")
        return False
    if art_data is None:
        out(f"No Art found: {path}")
        return False

    resized = resize_image(art_data, new_size)
    success = embed_new_art(audio, art_mime, resized)

    if success:
        out(f"Art fixed!")
        return True
    return False

def load_embedded_art(audio):
    cls = audio.__class__.__name__

    match cls:
        case 'MP3' | 'ID3':
            for frame in audio.values():
                if isinstance(frame, APIC):
                    return frame.mime, frame.data
            return None, None
        case 'FLAC' | 'OggVorbis':
            pic = None
            if audio.pictures:
                pic = audio.pictures[0]
            if pic is None and "metadata_block_picture" in audio:
                pic = Picture(base64.b64decode(audio["metadata_block_picture"][0]))

            if pic is None: return None, None
            return pic.mime, pic.data
        case 'MP4':
            covers = audio.get("covr")
            if covers:
                cover = covers[0]
                mime = "image/jpeg" if cover.imageformat == MP4Cover.FORMAT_JPEG else "image/png"
                return mime, bytes(cover)
            return None, None

    return False, False

def embed_new_art(audio, mime, data):
    global out
    if mime != "image/jpeg":
        out(f"MIME type {mime} is not JPEG")
        return False

    cls = audio.__class__.__name__

    match cls:
        case 'MP3' | 'ID3':
            audio.tags.delall("APIC")
            audio.tags.add(APIC(
                encoding=3,
                mime=mime,
                type=3,
                desc="cover",
                data=data
            ))
            audio.save(v2_version=3)
            return True
        case 'FLAC' | 'OggVorbis':
            audio.clear_pictures()

            pic = Picture()
            pic.mime = mime
            pic.type = 3
            pic.desc = "cover"
            pic.data = data
            audio.add_picture(pic)

            audio.save()
            return True
        case 'MP4':
            cover = MP4Cover(data, imageformat=MP4Cover.FORMAT_JPEG)
            audio["covr"] = [cover]
            audio.save()
            return True

    out(f"Invalid Format: {cls}")
    return False

def resize_image(data, new_size):
    img = Image.open(BytesIO(data))
    img = img.convert('RGB')

    # crop if needed, and resize
    img = _crop_to_square(img)
    img = img.resize((new_size, new_size), Resampling.LANCZOS)

    outimg = BytesIO()
    img.save(outimg, format='JPEG', quality=90)
    return outimg.getvalue()

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