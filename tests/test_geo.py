from exiffusion.geo import reverse_geo_code


def test_geo_code_standard():
    location = reverse_geo_code(51.5073219, -0.1276474)
    assert location.latitude == 51.5073219
    assert location.longitude == -0.1276474
    assert location.city == "City of Westminster"
    assert location.state == "England"
    assert location.country == "United Kingdom"
    assert location.country_code == "gb"
