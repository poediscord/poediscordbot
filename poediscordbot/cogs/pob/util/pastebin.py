import base64
import re
import urllib
import zlib
from urllib.error import HTTPError
from urllib.request import Request

import defusedxml.ElementTree as ET
from retrying import retry

from poediscordbot.util.logging import log

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
    content=re.sub('[<>]', '', content)

    if 'raw' in content:
        content = content.replace('raw/', '')
    regex = r"pastebin.com\/(\S+)"
    results = re.findall(regex, content)
    return results


def decode_base64_and_inflate(b64string):
    try:
        decoded_data = base64.b64decode(b64string)
        return zlib.decompress(decoded_data)
    except zlib.error as err:
        log.error(f"ZLib Error in paste: err={err}. Data={b64string}")
    except ValueError as err:
        log.error(f"Value Error in paste: err={err}")


def decode_to_xml(enc, encoding='windows-1252'):
    enc = enc.replace("-", "+").replace("_", "/")
    xml_str = decode_base64_and_inflate(enc)
    log.debug(f"XML={xml_str}")
    xml = None
    try:
        xml = ET.fromstring(xml_str.decode(encoding))
    except TypeError as err:
        log.debug(f"Could not parse the pastebin as xml msg={err}")

    return xml


def urllib_error_retry(attempt_number, ms_since_first_attempt):
    delay = 1 * (2 ** (attempt_number - 1))
    log.error(f"An error occurred during get_url_data(). Sleeping for {delay:.0f}s before retrying...")
    return delay * 1000


def fetch_code_from_html(html_content):
    """
    Sometimes pastebin's raw url does not let us get the raw data thus parse the code from the page's textfield with id
    'paste_code'
    :param html_content: html content we got
    :return: code or None
    """
    regex = r'\"paste_code\".*?>(?P<code>.*?)<'
    try:
        return re.search(regex, html_content).group("code")
    except IndexError:
        raise CaptchaError("Pastebin captcha cleared after accessing, could not parse html page."
                           "Please reupload and clear captchas before retrying.")


@retry(wait_exponential_multiplier=1000,
       stop_max_attempt_number=2,
       wait_func=urllib_error_retry)
def get_raw_data(url):
    q = Request(url, headers={
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    })
    try:
        url = urllib.request.urlopen(q)
    except HTTPError:
        return None
    content = url.read().decode('utf-8')
    if "Possible Spam Detected" in content:
        raise CaptchaError("Pastebin marked this as possible spam. Please reupload and clear captchas before retrying.")
    if "<!DOCTYPE HTML>" in content and "paste_code" in content:
        code = fetch_code_from_html(content)
        content = code
    return content  # read and encode as utf-8


def get_as_xml(paste_key):
    raw_url = 'https://pastebin.com/raw/' + paste_key
    log.debug(f"Retrieved from raw_url={raw_url}")
    data = get_raw_data(raw_url)
    return data


class CaptchaError(Exception):
    def __init__(self, message):
        self.message = message


class CaptchaError(Exception):
    def __init__(self, message):
        self.message = message
