from PIL import Image, ExifTags
from pillow_heif import register_heif_opener

register_heif_opener()


def get_exif(img):
    image = Image.open(img)

    exif = {
        ExifTags.TAGS[k]: v
        for k, v in image.getexif().items()
        if k in ExifTags.TAGS
    }

    return exif
