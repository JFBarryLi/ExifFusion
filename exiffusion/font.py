# https://github.com/python-pillow/Pillow/issues/4808
import logging
from pathlib import PosixPath
from importlib.resources import files

from fontTools.ttLib import TTFont

log = logging.getLogger(__name__)


def has_glyph(font: TTFont, glyph: str) -> bool:
    for table in font["cmap"].tables:
        if ord(glyph) in table.cmap.keys():
            return True

    log.debug(f"{font} does not have {glyph}")
    return False


def get_font(text: str) -> str | PosixPath:
    text = text.replace("\n", "")

    font_options = [
        files("exiffusion.assets").joinpath("WorkSans-Medium.otf"),
        files("exiffusion.assets").joinpath("unifont-15.1.05.otf"),
    ]

    for font_name in font_options:
        font = TTFont(font_name)
        if all(has_glyph(font, c) for c in text):
            return font_name

        log.info(f"{font_name} does not have all the glyphs for {text}.")

    log.warning(f"No suitable font for {text}.")
    log.info(f"Defaulting font to {font_options[-1]}.")
    return font_options[-1]
