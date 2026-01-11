from PIL.Image import Resampling
from mutagen.id3 import ID3, APIC
from io import BytesIO
from PIL import Image

def fix(path):
    pass

def _resize_image(data, new_size):
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

# TESTING

def _make_test_image(wh=800, color=(255, 0, 0)):
    img = Image.new('RGB', (wh,wh), color)
    buf = BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()

def _test_resize_image():
    original = _make_test_image(900)
    resized = _resize_image(original, 600)

    img = Image.open(BytesIO(resized))
    print(img.size)
    assert max(img.size) == 600
    assert img.format == 'JPEG'

if __name__ == '__main__':
    _test_resize_image()