from exiffusion.geo import dms_to_degrees
from exiffusion.geo import reverse_geo_code


def test_dms_to_degrees():
    GPSLatitudeRef = "N"
    GPSLatitude = (46.0, 28.0, 15.79)
    GPSLongitudeRef = "E"
    GPSLongitude = (30.0, 44.0, 28.3)

    latlng = dms_to_degrees(GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude)

    assert round(latlng.latitude, 8) == 46.47105278
    assert round(latlng.longitude, 8) == 30.74119444


def test_reverse_geo_code():
    location = reverse_geo_code(51.5073219, -0.1276474)
    assert location.latitude == 51.5073219
    assert location.longitude == -0.1276474
    assert location.city == "City of Westminster"
    assert location.state == "England"
    assert location.country == "United Kingdom"
    assert location.country_code == "gb"
