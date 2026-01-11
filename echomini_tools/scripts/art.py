from mutagen import File
from mutagen.id3 import APIC
from mutagen.flac import Picture
from mutagen.mp4 import MP4Cover
from mutagen.oggvorbis import OggVorbis

from PIL.Image import Resampling
from io import BytesIO
from PIL import Image

def fix(path, new_size=600):
    audio = File(path)

    art_mime, art_data = load_embedded_art(audio)
    if art_data is None: return None

    resized = resize_image(art_data, new_size)
    embed_new_art(audio, art_mime, resized)

    return path

def load_embedded_art(audio):
    cls = audio.__class__.__name__
    print(f"File is of type {cls}")

    match cls:
        case 'MP3' | 'ID3':
            for frame in audio.values():
                if isinstance(frame, APIC):
                    print("Found Art!")
                    return frame.mime, frame.data
            print("No Art found")
            return None
        case 'FLAC' | 'OggVorbis':
            if audio.pictures:
                pic = audio.pictures[0]
                print("Found Art!")
                return pic.mime, pic.data
            print("No Art found")
            return None
        case 'MP4':
            covers = audio.get("covr")
            if covers:
                cover = covers[0]
                mime = "image/jpeg" if cover.imageformat == MP4Cover.FORMAT_JPEG else "image/png"
                print("Found Art!")
                return mime, bytes(cover)
            print("No Art found")
            return None
        case 'OggVorbis':
            if audio.pictures:
                pic = audio.pictures[0]
                print("Found Art!")
                return pic.mime, pic.data
            print("No Art found")
            return None

    print("Invalid Format")
    return None

def embed_new_art(audio, mime, data):
    cls = audio.__class__.__name__

    if mime != "image/jpeg":
        print("Error, mime must be JPEG!")
        return False

    match cls:
        case 'MP3' | 'ID3':
            audio.delall("APIC")
            audio.add(APIC(
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

    print("Invalid Format")
    return False

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