from . import EXAMPLE_SOURCE_DIR

from exiffusion.extract_exif import get_exif


def test_get_exif():
    img = EXAMPLE_SOURCE_DIR / "odesa.HEIC"
    exif_data = get_exif(img)

    assert exif_data.Orientation == 1
    assert exif_data.DateTime == "2023:09:25 16:29:37"
    assert exif_data.GPSLatitudeRef == "N"
    assert exif_data.GPSLatitude == (46.0, 28.0, 15.79)
    assert exif_data.GPSLongitudeRef == "E"
    assert exif_data.GPSLongitude == (30.0, 44.0, 28.3)
