from importlib.resources import files
from pathlib import PosixPath
import logging

from PIL import ImageFont, ImageDraw, Image
from pillow_heif import register_heif_opener

from . import ROOT_DIR

register_heif_opener()

log = logging.getLogger(__name__)


def overlay_text(image: str | PosixPath, text: str):
    log.info(f"Overlaying text on {image}.")
    img = Image.open(image)

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    text_color = (255, 255, 255)

    draw.text(
        (width - right - margin, height - bottom - margin), text, text_color, font=font
    )

    output_name = image.name if image is PosixPath else image.split("/")[-1]

    img.save(ROOT_DIR / f"output/{output_name}")
