import re

import requests


def starts_with(prefix, string):
    return bool(re.match(prefix, string, re.I))


def fetch_xyz_pob_token(payload, version="latest"):
    """
    fetch the token used for pob party
    :param payload: pob payload
    :param version: either v3.7.0 or latest for the latest one
    :return:
    """
    url = f"https://pob.party/kv/put?ver={version}"
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()['url']
