from PIL import Image
from PIL.Image import Exif
from PIL.ExifTags import TAGS, GPSTAGS
from pillow_heif import register_heif_opener

from typing import Tuple
from pydantic import BaseModel
from pathlib import PosixPath
import logging

register_heif_opener()

GPSINFO_IFD_KEY = 34853
GENERAL_IFD_KEY = 34665

log = logging.getLogger(__name__)


class TopLevelExifTags(BaseModel):
    Orientation: int = 1
    DateTime: str
    Make: str = None
    Model: str = None
    HostComputer: str = None
    Software: str = None


class GPSExifTags(BaseModel):
    GPSLatitudeRef: str = None
    GPSLatitude: Tuple[float, float, float] = None
    GPSLongitudeRef: str = None
    GPSLongitude: Tuple[float, float, float] = None


class GeneralIFDTags(BaseModel):
    ShutterSpeedValue: float = None
    ApertureValue: float = None
    DateTimeOriginal: str = None
    DateTimeDigitized: str = None
    BrightnessValue: float = None
    ExposureBiasValue: float = None
    MeteringMode: int = None
    ColorSpace: int = None
    Flash: int = None
    FocalLength: float = None
    ExifImageWidth: int = None
    ExifImageHeight: int = None
    FocalLengthIn35mmFilm: int = None
    OffsetTime: str = None
    SubsecTimeOriginal: str = None
    SubjectLocation: Tuple[int, int, int, int] = None
    SubsecTimeDigitized: str = None
    SensingMethod: int = None
    ExposureTime: float = None
    FNumber: float = None
    SceneType: int = None
    ExposureProgram: int = None
    ISOSpeedRatings: int = None
    ExposureMode: int = None
    WhiteBalance: int = None
    LensSpecification: Tuple[float, float, float, float] = None
    LensMake: str = None
    LensModel: str = None
    CompositeImage: int = None
    # MakerNote: bytes


class RelevantExifTags(TopLevelExifTags, GPSExifTags, GeneralIFDTags):
    pass


def get_exif(img: str | PosixPath, get_detailed_tags=False) -> RelevantExifTags:
    log.info(f"Getting Exif data from {img}.")

    image = Image.open(img)
    exif = image.getexif()

    relevant_tags = [
        "Orientation",
        "DateTime",
        "Make",
        "Model",
        "HostComputer",
        "Software",
    ]

    exif_tags = {}

    for tag, value in exif.items():
        if tag in TAGS:
            if TAGS[tag] in relevant_tags:
                exif_tags[TAGS[tag]] = value

    gps_tags = get_gps(exif)

    if get_detailed_tags:
        general_tags = get_general_ifd(exif)

        return RelevantExifTags(
            **(exif_tags | gps_tags.model_dump() | general_tags.model_dump())
        )
    else:
        return RelevantExifTags(**(exif_tags | gps_tags.model_dump()))


def get_gps(exif: Exif) -> GPSExifTags:
    gps_info = exif.get_ifd(GPSINFO_IFD_KEY)

    relevant_tags = ["GPSLatitudeRef", "GPSLatitude", "GPSLongitudeRef", "GPSLongitude"]

    gps_tags = {}

    for tag, value in gps_info.items():
        gps_tag = GPSTAGS.get(tag, tag)
        if gps_tag in relevant_tags:
            gps_tags[gps_tag] = value

    return GPSExifTags(**gps_tags)


def get_general_ifd(exif: Exif) -> GeneralIFDTags:
    general_ifd = exif.get_ifd(GENERAL_IFD_KEY)

    relevant_tags = [
        "ShutterSpeedValue",
        "ApertureValue",
        "DateTimeOriginal",
        "DateTimeDigitized",
        "BrightnessValue",
        "ExposureBiasValue",
        "MeteringMode",
        "ColorSpace",
        "Flash",
        "FocalLength",
        "ExifImageWidth",
        "ExifImageHeight",
        "FocalLengthIn35mmFilm",
        "OffsetTime",
        "SubsecTimeOriginal",
        "SubjectLocation",
        "SubsecTimeDigitized",
        "SensingMethod",
        "ExposureTime",
        "FNumber",
        "SceneType",
        "ExposureProgram",
        "ISOSpeedRatings",
        "ExposureMode",
        "WhiteBalance",
        "LensSpecification",
        "LensMake",
        "LensModel",
        "CompositeImage",
        # "MakerNote",
    ]

    ifd_tags = {}

    for tag, value in general_ifd.items():
        ifd_tag = TAGS.get(tag, tag)

        if ifd_tag in relevant_tags:
            ifd_tags[ifd_tag] = value

    if "SceneType" in ifd_tags:
        ifd_tags["SceneType"] = ord(ifd_tags["SceneType"])

    return GeneralIFDTags(**ifd_tags)
