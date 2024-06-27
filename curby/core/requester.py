import functools

import requests

from .utils import hash_dict

@hash_dict
@functools.lru_cache()
def request(url: str, header={}, params={}):
    return requests.get(url, headers=header, params=params)