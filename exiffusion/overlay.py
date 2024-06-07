from importlib.resources import files

from PIL import ImageFont, ImageDraw, Image
from pillow_heif import register_heif_opener

from . import ROOT_DIR

register_heif_opener()


def overlay_text(image: str, text: str):
    img = Image.open(image)

    font_size = max(img.size) * 0.025
    font_path = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = ImageFont.truetype(font_path, font_size)
    width, height = img.size
    margin = font_size

    draw = ImageDraw.Draw(img)

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)

    calc_text_color(
        img,
        width - right - margin,
        height - bottom - margin,
        width - margin,
        height - margin,
    )
    text_color = (255, 255, 255)

    draw.text(
        (width - right - margin, height - bottom - margin), text, text_color, font=font
    )

    img.save(ROOT_DIR / f'output/{image.split('/')[-1]}')


def calc_text_color(img: Image, left: int, top: int, right: int, bottom: int):
    pass
