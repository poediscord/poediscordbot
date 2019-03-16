import base64
import re
import urllib
import zlib
from urllib.request import Request

import defusedxml.ElementTree as ET
from retrying import retry

from src.util.logging import log

'''
Original from: https://github.com/aggixx/PoBPreviewBot/blob/master/util.py 
            && https://github.com/aggixx/PoBPreviewBot/blob/master/pastebin.py
'''


def fetch_paste_key(content):
    """
    Fetches the last paste key in a message.
    :param content: message.content
    :return: paste key to retrieve pastebin content
    """
    if 'raw' in content:
        content = content.replace('raw/', '')
    regex = r"pastebin.com\/(\S*)"
    results = re.findall(regex, content)
    return results


def decode_base64_and_inflate(b64string):
    try:
        decoded_data = base64.b64decode(b64string)
        return zlib.decompress(decoded_data)
    except zlib.error as err:
        log.error("ZLib Error in paste: err={}".format(err))
    except ValueError as err:
        log.error("Value Error in paste: err={}".format(err))


def decode_to_xml(enc):
    enc = enc.replace("-", "+").replace("_", "/")
    xml_str = decode_base64_and_inflate(enc)
    log.debug("XML={}".format(xml_str))
    xml = None
    try:
        xml = ET.fromstring(xml_str)
    except TypeError as err:
        log.debug("Could not parse the pastebin as xml msg={}".format(err))

    return xml


def urllib_error_retry(attempt_number, ms_since_first_attempt):
    delay = 1 * (2 ** (attempt_number - 1))
    log.error("An error occurred during get_url_data(). Sleeping for {:.0f}s before retrying...".format(delay))
    return delay * 1000


@retry(wait_exponential_multiplier=1000,
       stop_max_attempt_number=2,
       wait_func=urllib_error_retry)
def get_raw_data(url):
    q = Request(url)
    q.add_header('Cache-Control', 'max-age=0')
    url = urllib.request.urlopen(q)
    content = url.read().decode('utf-8')
    if "Possible Spam Detected" in content:
        raise CaptchaError("Pastebin marked this as possible spam. Please reupload and clear captchas before retrying.")

    return content  # read and encode as utf-8


def get_as_xml(paste_key):
    raw_url = 'https://pastebin.com/raw/' + paste_key
    log.debug("Retrieved from raw_url={}".format(raw_url))
    data = get_raw_data(raw_url)
    return decode_to_xml(data)


class CaptchaError(Exception):
    def __init__(self, message):
        self.message = message


class CaptchaError(Exception):
    def __init__(self, message):
        self.message = message
