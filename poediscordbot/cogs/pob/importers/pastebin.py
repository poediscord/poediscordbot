import re
import urllib
from urllib.error import HTTPError
from urllib.request import Request

from retrying import retry

from poediscordbot.cogs.pob.importers.abstract_importer import AbstractImporter
from poediscordbot.util.logging import log

'''
Original from: https://github.com/aggixx/PoBPreviewBot/blob/master/util.py 
            && https://github.com/aggixx/PoBPreviewBot/blob/master/pastebin.py
'''


class PastebinImporter(AbstractImporter):
    def get_source_url(self, paste_key) -> str:
        return f'https://pastebin.com/{paste_key}'

    def _get_raw_url(self, paste_key) -> str:
        return f'https://pastebin.com/raw/{paste_key}'

    def fetch_data(self, paste_key):
        raw_url = self._get_raw_url(paste_key)
        log.debug(f"Retrieved from raw_url={raw_url}")
        data = self.__get_raw_data(raw_url)
        return data

    def _parse_url(self, url) -> [str]:
        if 'raw' in url:
            url = url.replace('raw/', '')
        regex = r"pastebin.com\/(\S+)"
        results = re.findall(regex, url)
        return results

    @retry(wait_exponential_multiplier=1000,
           stop_max_attempt_number=2,
           wait_func=AbstractImporter._backoff_wait_fn)
    def __get_raw_data(self, url):
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
            raise CaptchaError(
                "Pastebin marked this as possible spam. Please reupload and clear captchas before retrying.")
        if "<!DOCTYPE HTML>" in content and "paste_code" in content:
            code = self.__fetch_code_from_html(content)
            content = code
        return content  # read and encode as utf-8

    def __fetch_code_from_html(hself, html_content):
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


class CaptchaError(Exception):
    def __init__(self, message):
        self.message = message
