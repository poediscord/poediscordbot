import re

import requests


def starts_with(prefix, string):
    return bool(re.match(prefix, string, re.I))


def fetch_xyz_pob_token(payload, version="3.7.0"):
    url = f"https://pob.party/kv/put?ver=v{version}"
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()['url']
