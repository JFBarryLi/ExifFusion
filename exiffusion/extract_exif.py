from PIL import Image
from PIL.Image import Exif
from PIL.ExifTags import TAGS, GPSTAGS
from pillow_heif import register_heif_opener

register_heif_opener()

GPSINFO_IFD_KEY = 34853


def get_exif(img) -> Exif:
    image = Image.open(img)
    exif = image.getexif()

    exif_tags = {}

    for tag, value in exif.items():
        if tag in TAGS:
            exif_tags[TAGS[tag]] = value

    gps_tags = get_gps(exif)

    return exif_tags | gps_tags


def get_gps(exif):
    gps_info = exif.get_ifd(GPSINFO_IFD_KEY)

    gps_tags = {}

    for tag, value in gps_info.items():
        gps_tags[GPSTAGS.get(tag, tag)] = value

    return gps_tags
