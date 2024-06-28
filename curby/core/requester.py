import requests
from cachetools.func import ttl_cache

from .common import REFRESH_TTL
from .utils import hash_dict

@hash_dict
@ttl_cache(ttl=REFRESH_TTL)
def request(url: str, header={}, params={}):
    return requests.get(url, headers=header, params=params)