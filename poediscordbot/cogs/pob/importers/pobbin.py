import re

import requests
from retrying import retry

from poediscordbot.cogs.pob.importers.abstract_importer import AbstractImporter
from poediscordbot.util.logging import log


class PobBinImporter(AbstractImporter):

    def _get_raw_url(self, paste_key) -> str:
        return f'https://pobb.in/{paste_key}/raw'

    def get_source_url(self, paste_key) -> str:
        return f'https://pobb.in/{paste_key}'

    def fetch_data(self, paste_key):
        raw_url = self._get_raw_url(paste_key)
        log.debug(f"Retrieved from raw_url={raw_url}")
        data = self.__get_raw_data(raw_url)
        return data

    def _parse_url(self, url) -> [str]:
        if 'raw' in url:
            url = url.replace('/raw', '')
        regex = r"pobb.in\/(\S+)"
        results = re.findall(regex, url)
        return results

    @retry(wait_exponential_multiplier=1000,
           stop_max_attempt_number=2,
           wait_func=AbstractImporter._backoff_wait_fn)
    def __get_raw_data(self, url):
        headers = {
            'User-Agent': 'pob discord bot (https://github.com/poediscord/poediscordbot)'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(response.text)
            return None
        content = response.text
        return content  # read and encode as utf-8
