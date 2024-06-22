import functools
import logging

from typing import Tuple, Optional
from pydantic import BaseModel

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

log = logging.getLogger(__name__)

geolocator = Nominatim(user_agent="ExifFusion")

reverse_limit = RateLimiter(
    geolocator.reverse,
    min_delay_seconds=1,
    max_retries=4,
)

reverse = functools.lru_cache(maxsize=1024)(functools.partial(reverse_limit, timeout=5))


class Location(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: float
    longitude: float
    neighbourhood: Optional[str] = None
    subdivision: Optional[str] = None
    suburb: Optional[str] = None
    borough: Optional[str] = None
    city_district: Optional[str] = None
    village: Optional[str] = None
    town: Optional[str] = None
    city: Optional[str] = None
    municipality: Optional[str] = None
    region: Optional[str] = None
    county: Optional[str] = None
    state_district: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None


class LatLng(BaseModel):
    latitude: float
    longitude: float


def dms_to_location(
    GPSLatitudeRef: str,
    GPSLatitude: Tuple[float, float, float],
    GPSLongitudeRef: str,
    GPSLongitude: Tuple[float, float, float],
) -> Location:
    latlng = dms_to_degrees(GPSLatitudeRef, GPSLatitude, GPSLongitudeRef, GPSLongitude)

    location = reverse_geo_code(latlng.latitude, latlng.longitude)

    return location


def dms_to_degrees(
    GPSLatitudeRef: str,
    GPSLatitude: Tuple[float, float, float],
    GPSLongitudeRef: str,
    GPSLongitude: Tuple[float, float, float],
) -> LatLng:
    lat_sign = -1 if GPSLatitudeRef == "S" else 1
    lng_sign = -1 if GPSLongitudeRef == "W" else 1

    latitude = lat_sign * (GPSLatitude[0] + GPSLatitude[1] / 60 + GPSLatitude[2] / 3600)
    longitude = lng_sign * (
        GPSLongitude[0] + GPSLongitude[1] / 60 + GPSLongitude[2] / 3600
    )

    return LatLng(latitude=latitude, longitude=longitude)


def reverse_geo_code(lat: float, lng: float) -> Location:
    try:
        rev = reverse((lat, lng), language="en", addressdetails=True)

        rev_address = rev.raw.get("address")
        rev_name = rev.raw.get("name")

        log.info(f"Reverse geocoding: {lat}, {lng}.")
        if rev_address is None:
            return Location(
                **{
                    "name": rev_name if rev_name != "" else None,
                    "address": rev.address if rev.address != "" else None,
                    "latitude": lat,
                    "longitude": lng,
                    "neighbourhood": None,
                    "subdivision": None,
                    "suburb": None,
                    "borough": None,
                    "city_district": None,
                    "village": None,
                    "town": None,
                    "city": None,
                    "municipality": None,
                    "region": None,
                    "county": None,
                    "state_district": None,
                    "district": None,
                    "state": None,
                    "country": None,
                    "country_code": None,
                }
            )
        else:
            return Location(
                **{
                    "name": rev_name if rev_name != "" else None,
                    "address": rev.address if rev.address != "" else None,
                    "latitude": lat,
                    "longitude": lng,
                    "neighbourhood": rev_address.get("neighbourhood"),
                    "subdivision": rev_address.get("subdivision"),
                    "suburb": rev_address.get("suburb"),
                    "borough": rev_address.get("borough"),
                    "city_district": rev_address.get("city_district"),
                    "village": rev_address.get("village"),
                    "town": rev_address.get("town"),
                    "city": rev_address.get("city"),
                    "municipality": rev_address.get("municipality"),
                    "region": rev_address.get("region"),
                    "county": rev_address.get("county"),
                    "state_district": rev_address.get("state_district"),
                    "district": rev_address.get("district"),
                    "state": rev_address.get("state"),
                    "country": rev_address.get("country"),
                    "country_code": rev_address.get("country_code"),
                }
            )
    except Exception as e:
        log.error(f"Failed to reverse geocode: {lat}, {lng}. Exception: {e}.")
        return Location(
            **{
                "name": None,
                "address": None,
                "latitude": lat,
                "longitude": lng,
                "neighbourhood": None,
                "subdivision": None,
                "suburb": None,
                "borough": None,
                "city_district": None,
                "village": None,
                "town": None,
                "city": None,
                "municipality": None,
                "region": None,
                "county": None,
                "state_district": None,
                "district": None,
                "state": None,
                "country": None,
                "country_code": None,
            }
        )
