from pathlib import Path, PosixPath
from datetime import datetime
import os
import logging

from exiffusion.extract_exif import get_exif
from exiffusion.geo import dms_to_location
from exiffusion.overlay import overlay_text

log = logging.getLogger(__name__)


def fuse_exif(path: str | PosixPath):
    if os.path.isdir(path):
        heic = sorted(Path(path).glob("*.heic", case_sensitive=False))
        jpg = sorted(Path(path).glob("*.jpg", case_sensitive=False))
        jpeg = sorted(Path(path).glob("*.jpeg", case_sensitive=False))

        imgs = heic + jpg + jpeg
    elif os.path.isfile(path):
        imgs = [Path(path)]

    for img in imgs:
        log.info(f"Processing: {img}")
        try:
            exif_tags = get_exif(img)

            location = dms_to_location(
                exif_tags.GPSLatitudeRef,
                exif_tags.GPSLatitude,
                exif_tags.GPSLongitudeRef,
                exif_tags.GPSLongitude,
            )

            formatted_datetime = datetime.strptime(
                exif_tags.DateTime, "%Y:%m:%d %H:%M:%S"
            ).strftime("%Y-%m-%d %H:%M:%S")

            text = f"{formatted_datetime}\n{location.city}, {location.country}\n{round(location.latitude, 4)}, {round(location.longitude, 4)}"
            overlay_text(img, text)
        except Exception as e:
            log.error(f"Failed to process {img}. Error: {e}")

    return imgs
