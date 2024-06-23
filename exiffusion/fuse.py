from pathlib import Path, PosixPath
from datetime import datetime
import os
import logging

from typing import List

from rich.progress import track

from exiffusion.exif import get_exif
from exiffusion.geo import dms_to_location
from exiffusion.overlay import overlay_text

log = logging.getLogger(__name__)


def fuse_exif(path: str | PosixPath, output_dir: str | PosixPath):
    imgs = []

    if os.path.isdir(path):
        heic = sorted(Path(path).glob("*.heic", case_sensitive=False))
        jpg = sorted(Path(path).glob("*.jpg", case_sensitive=False))
        jpeg = sorted(Path(path).glob("*.jpeg", case_sensitive=False))

        imgs = heic + jpg + jpeg
    elif os.path.isfile(path):
        imgs = [Path(path)]

    if len(imgs) == 0:
        log.info("No valid images found.")
        return

    imgs = process_images(imgs, output_dir)

    return imgs


def process_images(
    imgs: List[str | PosixPath], output_dir: str | PosixPath
) -> List[str | PosixPath]:
    successes = []
    failures = []

    for img in track(imgs, description="Processing..."):
        log.info(f"Processing: {img}")
        try:
            exif_tags = get_exif(img)

            formatted_datetime = datetime.strptime(
                exif_tags.DateTime, "%Y:%m:%d %H:%M:%S"
            ).strftime("%Y-%m-%d %H:%M:%S")

            if (
                exif_tags.GPSLatitude is not None
                and exif_tags.GPSLatitudeRef is not None
                and exif_tags.GPSLongitude is not None
                and exif_tags.GPSLongitudeRef is not None
            ):
                location = dms_to_location(
                    exif_tags.GPSLatitudeRef,
                    exif_tags.GPSLatitude,
                    exif_tags.GPSLongitudeRef,
                    exif_tags.GPSLongitude,
                )

                text = f"{formatted_datetime}"

                if location.country is not None:
                    if location.village is not None and len(location.village) <= 30:
                        text += f"\n{location.village}, {location.country}"
                    elif location.town is not None and len(location.town) <= 30:
                        text += f"\n{location.town}, {location.country}"
                    elif location.city is not None and len(location.city) <= 30:
                        text += f"\n{location.city}, {location.country}"
                    elif (
                        location.municipality is not None
                        and len(location.municipality) <= 30
                    ):
                        text += f"\n{location.municipality}, {location.country}"
                    elif location.name is not None and len(location.name) <= 30:
                        text += f"\n{location.name}, {location.country}"
                    elif location.region is not None and len(location.region) <= 30:
                        text += f"\n{location.region}, {location.country}"
                    elif location.county is not None and len(location.county) <= 30:
                        text += f"\n{location.county}, {location.country}"
                    elif (
                        location.state_district is not None
                        and len(location.state_district) <= 30
                    ):
                        text += f"\n{location.state_district}, {location.country}"
                    elif location.district is not None and len(location.district) <= 30:
                        text += f"\n{location.district}, {location.country}"
                    elif location.state is not None and len(location.state) <= 30:
                        text += f"\n{location.state}, {location.country}"
                    elif (
                        location.address is not None
                        and len(location.address.split(",")[0]) <= 30
                    ):
                        text += (
                            f"\n{location.address.split(',')[0]}, {location.country}"
                        )
                    elif (
                        location.latitude is not None and location.longitude is not None
                    ):
                        text += f"\n{round(location.latitude, 4)}, {round(location.longitude, 4)}\n{location.country}"
                else:
                    text = f"{formatted_datetime}"
            else:
                text = f"{formatted_datetime}"

            overlay_text(img, text, output_dir, exif_tags.Orientation)
            successes.append(img)
        except Exception as e:
            log.error(f"Failed to process {img}. Error: {e}")
            failures.append(img)

    log.info(f"Successfully processed: {successes}.")

    if failures:
        log.warn(f"Failed to process: {failures}")

    return imgs
