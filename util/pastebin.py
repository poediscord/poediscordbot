import logging
import re
import base64
import zlib
import defusedxml.ElementTree as ET
import urllib.request
from retrying import retry
from util.logging import log

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
    regex = r".*pastebin.com\/(\S*)"
    results = re.findall(regex, content)
    return results[0]


def decode_base64_and_inflate(b64string):
    try:
        decoded_data = base64.b64decode(b64string)
        return zlib.decompress(decoded_data)
    except zlib.error:
        pass
    except ValueError as err:
        pass


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
       stop_max_attempt_number=1,
       wait_func=urllib_error_retry)
def get_raw_data(url):
    url = urllib.request.urlopen(url)
    return url.read().decode('utf-8')  # read and encode as utf-8


def get_as_xml(paste_key):
    raw_url = 'https://pastebin.com/raw/' + paste_key
    log.debug("Retrieved from raw_url={}".format(raw_url))
    data = get_raw_data(raw_url)
    return decode_to_xml(data)
