from io import BytesIO
from PIL import Image
from mutagen.flac import Picture
from mutagen.id3 import APIC
from mutagen.mp4 import MP4Cover

from echomini_tools.scripts.art import resize_image, load_embedded_art

def _make_test_image(wh=800, color=(255, 0, 0)):
    img = Image.new('RGB', (wh,wh), color)
    buf = BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()

def _test_resize_image():
    original = _make_test_image(900)
    resized = resize_image(original, 600)

    img = Image.open(BytesIO(resized))
    assert max(img.size) == 600
    assert img.format == 'JPEG'

class _FakeFLAC:
    __class__ = type("FLAC",(),{})

    def __init__(self):
        super().__init__()
        pic = Picture()
        pic.mime = "image/jpeg"
        pic.data = b"JPEGDATA"
        self.pictures = [pic]

class _FakeMP3(dict):
    __class__ = type("MP3",(),{})

    def __init__(self):
        super().__init__()
        self["APIC:"] = APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="cover",
            data=b"JPEGDATA"
        )

class _FakeOGG:
    __class__ = type("OggVorbis",(),{})

    def __init__(self):
        super().__init__()
        pic = Picture()
        pic.mime = "image/jpeg"
        pic.data = b"JPEGDATA"
        self.pictures = [pic]

class _FakeM4A(dict):
    __class__ = type("MP4",(),{})
    def __init__(self):
        super().__init__()
        self["covr"] = [MP4Cover(b"JPEGDATA", imageformat=MP4Cover.FORMAT_JPEG)]

def _test_embedded_art_loader(file):
    mime, data = load_embedded_art(file)
    assert mime == "image/jpeg"
    assert data == b"JPEGDATA"

if __name__ == '__main__':
    _test_resize_image()
    print("✅ art.py: resize_image()\n")
    _test_embedded_art_loader(_FakeFLAC())
    print("✅ art.py: load_embedded_art(FLAC)\n")
    _test_embedded_art_loader(_FakeMP3())
    print("✅ art.py: load_embedded_art(MP3)\n")
    _test_embedded_art_loader(_FakeOGG())
    print("✅ art.py: load_embedded_art(OGG)\n")
    _test_embedded_art_loader(_FakeM4A())
    print("✅ art.py: load_embedded_art(M4A)\n")
