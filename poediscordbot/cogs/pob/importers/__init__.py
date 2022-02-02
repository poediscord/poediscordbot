from poediscordbot.cogs.pob.importers.abstract_importer import AbstractImporter


class PasteData:
    __slots__ = 'key', 'source_url', 'source_site'

    def __init__(self, key: str, source_url: str, source_site: str):
        self.key = key
        self.source_url = source_url
        self.source_site = source_site
