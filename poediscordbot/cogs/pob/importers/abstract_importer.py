import re
from abc import ABC, abstractmethod

from poediscordbot.util.logging import log


class AbstractImporter(ABC):
    def __init__(self, message):
        self.keys = self.fetch_keys(message)

    @abstractmethod
    def fetch_data(self, paste_key):
        pass

    def fetch_keys(self, url):
        # strip < and > from discord msg
        url = re.sub('[<>]', '', url)
        return self._parse_url(url)

    @abstractmethod
    def get_source_url(self, paste_key) -> str:
        pass

    @abstractmethod
    def _parse_url(self, url) -> [str]:
        pass

    @staticmethod
    def _backoff_wait_fn(attempt_number):
        delay = 1 * (2 ** (attempt_number - 1))
        log.error(f"An error occurred during get_url_data(). Sleeping for {delay:.0f}s before retrying...")
        return delay * 1000

    @abstractmethod
    def _get_raw_url(self, paste_key) -> str:
        pass
