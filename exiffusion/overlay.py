from pathlib import PosixPath
from typing import Optional
import logging

from PIL import ImageFont, ImageDraw, Image
from pillow_heif import register_heif_opener

from exiffusion.color import Color, color_contrast
from exiffusion.font import get_font

register_heif_opener()

log = logging.getLogger(__name__)


def overlay_text(
    image: str | PosixPath,
    text: str,
    output_dir: str | PosixPath,
    orientation: Optional[int] = None,
):
    log.info(f"Overlaying text on {image}.")
    img = Image.open(image)

    if img.filename.lower().endswith(("jpg", "jpeg")):
        img = orient_image(img, orientation)

    font_size = max(img.size) * 0.025
    font_path = get_font(text)
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    text_color = calc_text_color(
        img,
        width - right - margin,
        height - bottom - margin,
        width - margin,
        height - margin,
    )

    draw.text(
        (width - right - margin, height - bottom - margin),
        text,
        (text_color.R, text_color.G, text_color.B),
        font=font,
    )

    output_name = image.name if type(image) is PosixPath else image.split("/")[-1]

    img.save(f"{output_dir}/{output_name}", exif=img.getexif())


def calc_text_color(img: Image, left: int, top: int, right: int, bottom: int) -> Color:
    # 1. Calculate the dominant color of the text background
    # 2. Use a color_contrast function to select white or black

    log.info(f"Calculating text overlay color for {img.filename}.")

    cropped_img = img.crop([left, top, right, bottom])
    cropped_img.filename = img.filename
    dominant_color = calc_dominant_color(cropped_img)

    white = Color(R=255, G=255, B=255)
    black = Color(R=0, G=0, B=0)

    white_contrast = color_contrast(white, dominant_color)
    black_contrast = color_contrast(black, dominant_color)

    return white if white_contrast > black_contrast else black


def calc_dominant_color(img: Image, palette_size: int = 4) -> Color:
    # Reference
    # https://stackoverflow.com/a/61730849

    log.info(f"Calculating dominant color for text overlay region: {img.filename}.")

    # Reduce colors (uses k-means internally)
    paletted = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index * 3 : palette_index * 3 + 3]

    log.info(
        f"Dominant color for text overlay region: {dominant_color}; {img.filename}"
    )
    return Color(R=dominant_color[0], G=dominant_color[1], B=dominant_color[2])


def calc_dominant_color_rescaling(img: Image) -> Color:
    image = img.copy()
    image = image.convert("RGBA")
    image = img.resize((1, 1), resample=0)
    dominant_color = image.getpixel((0, 0))

    log.info(
        f"Dominant color for text overlay region: {dominant_color}; {img.filename}"
    )

    return Color(R=dominant_color[0], G=dominant_color[1], B=dominant_color[2])


def orient_image(img: Image, orientation: Optional[int] = None) -> Image:
    if not orientation:
        return img

    file_name = img.filename
    oriented_img = img
    if orientation == 3:
        oriented_img = img.rotate(180, expand=True)
    elif orientation == 6:
        oriented_img = img.rotate(270, expand=True)
    elif orientation == 8:
        oriented_img == img.rotate(90, expand=True)

    oriented_img.filename = file_name
    return oriented_img
