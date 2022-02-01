import base64
import re
import zlib
from abc import ABC, abstractmethod

import defusedxml.ElementTree as ET

from poediscordbot.util.logging import log


class AbstractImporter(ABC):
    def __init__(self, message):
        self.keys=self.fetch_keys(message)

    @abstractmethod
    def fetch_data(self, url):
        pass

    def fetch_keys(self, url):
        # strip < and > from discord msg
        url = re.sub('[<>]', '', url)
        return self._parse_url(url)

    @abstractmethod
    def _parse_url(self, url) -> [str]:
        pass

    @staticmethod
    def _backoff_wait_fn(attempt_number, ms_since_first_attempt):
        delay = 1 * (2 ** (attempt_number - 1))
        log.error(f"An error occurred during get_url_data(). Sleeping for {delay:.0f}s before retrying...")
        return delay * 1000

    def __decode_base64_and_inflate(self, b64string):
        try:
            decoded_data = base64.b64decode(b64string)
            return zlib.decompress(decoded_data)
        except zlib.error as err:
            log.error(f"ZLib Error in paste: err={err}. Data={b64string}")
        except ValueError as err:
            log.error(f"Value Error in paste: err={err}")

    def decode_to_xml(self, enc, encoding='windows-1252'):
        enc = enc.replace("-", "+").replace("_", "/")
        xml_str = self.__decode_base64_and_inflate(enc)
        log.debug(f"XML={xml_str}")
        xml = None
        try:
            xml = ET.fromstring(xml_str.decode(encoding))
        except TypeError as err:
            log.debug(f"Could not parse the pastebin as xml msg={err}")

        return xml

