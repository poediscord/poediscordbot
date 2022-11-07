import re

import requests

from poediscordbot.util.logging import log


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
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            return response.json()['url']
        else:
            log.error(f"error while fetching pob party token: {response.status_code}: {response.text}")
    except Exception as err:
        log.error(f"error while fetching pob party token  {err}, {type(err)}")
    return ""
