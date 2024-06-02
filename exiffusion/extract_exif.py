from PIL import Image
from PIL.Image import Exif
from PIL.ExifTags import TAGS, GPSTAGS
from pillow_heif import register_heif_opener

from typing import Tuple, Union, Dict
from pydantic import BaseModel

register_heif_opener()

GPSINFO_IFD_KEY = 34853


# TODO: Handle missing fields
class RelevantExifTags(BaseModel):
    Orientation: int
    DateTime: str
    GPSLatitudeRef: str
    GPSLatitude: Tuple[float, float, float]
    GPSLongitudeRef: str
    GPSLongitude: Tuple[float, float, float]


def get_exif(img: str) -> RelevantExifTags:
    image = Image.open(img)
    exif = image.getexif()

    relevant_tags = ["Orientation", "DateTime"]

    exif_tags = {}

    for tag, value in exif.items():
        if tag in TAGS:
            if TAGS[tag] in relevant_tags:
                exif_tags[TAGS[tag]] = value

    gps_tags = get_gps(exif)

    return RelevantExifTags(**(exif_tags | gps_tags))


def get_gps(exif: Exif) -> Dict[str, Union[str, Tuple[float, float, float]]]:
    gps_info = exif.get_ifd(GPSINFO_IFD_KEY)

    relevant_tags = ["GPSLatitudeRef", "GPSLatitude", "GPSLongitudeRef", "GPSLongitude"]

    gps_tags = {}

    for tag, value in gps_info.items():
        gps_tag = GPSTAGS.get(tag, tag)
        if gps_tag in relevant_tags:
            gps_tags[gps_tag] = value

    return gps_tags
