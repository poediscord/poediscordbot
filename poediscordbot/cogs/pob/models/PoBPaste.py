from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.util.custom_json_parser import JsonifySlotsCls


class PobPaste(JsonifySlotsCls):
    __slots__ = "author_id", "author_name", "build", "pastebin_url"

    def __init__(self, author_id: int, author_name: str, build: Build, pastebin_url) -> None:
        self.author_id = author_id
        self.author_name = author_name
        self.build = build
        self.pastebin_url = pastebin_url
