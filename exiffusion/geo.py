import functools
import logging

from pydantic import BaseModel

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

log = logging.getLogger(__name__)

geolocator = Nominatim(user_agent="ExifFusion")

reverse_limit = RateLimiter(geolocator.reverse, min_delay_seconds=1)

reverse = functools.lru_cache(maxsize=1024)(functools.partial(reverse_limit, timeout=5))


class Location(BaseModel):
    address: str
    latitude: float
    longitude: float
    city: str
    state: str
    country: str
    country_code: str


def reverse_geo_code(lat, lng):
    try:
        rev = reverse((lat, lng), language="en")

        rev_address = rev.raw.get("address")

        log.info(f"Reverse geocoding: {lat}, {lng}.")
        return Location(
            **{
                "address": rev.address,
                "latitude": lat,
                "longitude": lng,
                "city": rev_address.get("city") if rev_address is not None else None,
                "state": rev_address.get("state") if rev_address is not None else None,
                "country": rev_address.get("country")
                if rev_address is not None
                else None,
                "country_code": rev_address.get("country_code")
                if rev_address is not None
                else None,
            }
        )
    except Exception as e:
        log.error(f"Failed to reverse geocode: {lat}, {lng}. Exception: {e}.")
        return {
            "address": None,
            "latitude": None,
            "longitude": None,
            "city": None,
            "state": None,
            "country": None,
            "country_code": None,
        }
