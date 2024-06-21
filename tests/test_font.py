from importlib.resources import files

from fontTools.ttLib import TTFont

from exiffusion.font import has_glyph, get_font


def test_get_font_latin():
    text = "Toronto, Canada"
    font = get_font(text)

    assert font == files("exiffusion.assets").joinpath("WorkSans-Medium.otf")


def test_get_font_cyryllic():
    text = "Привокзальна вулиця"
    font = get_font(text)

    assert font == files("exiffusion.assets").joinpath("unifont-15.1.05.otf")


def test_has_glyph_latin():
    font_name = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = TTFont(font_name)

    assert has_glyph(font, "A")


def test_has_glyph_cyryllic_false():
    font_name = files("exiffusion.assets").joinpath("WorkSans-Medium.otf")
    font = TTFont(font_name)

    assert not has_glyph(font, "П")


def test_has_glyph_cyryllic_trye():
    font_name = files("exiffusion.assets").joinpath("unifont-15.1.05.otf")
    font = TTFont(font_name)

    assert has_glyph(font, "П")
