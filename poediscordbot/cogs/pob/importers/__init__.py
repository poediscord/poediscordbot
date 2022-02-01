import dataclasses

from poediscordbot.cogs.pob.importers.abstract_importer import AbstractImporter


@dataclasses.dataclass
class PasteData:
    key: str
    source_url: str