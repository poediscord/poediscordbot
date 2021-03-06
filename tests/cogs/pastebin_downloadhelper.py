import xml.etree.ElementTree as ET

from poediscordbot.cogs.pob.util import pastebin
from poediscordbot.util.logging import log
from tests import get_test_path


class PastebinHelper:
    @staticmethod
    def to_file_name(name):
        validchars = "-_.() "
        out = ""
        for c in name:
            if str.isalpha(c) or str.isdigit(c) or (c in validchars):
                out += c
            else:
                out += "_"
        return out

    @staticmethod
    def fetch_pastebins(content: [str]):
        for line in content:
            line = line.strip()
            if "pastebin.com" in line:
                key = line.split("/")[-1]
                log.debug(f"Writing content for '{line}'")
                xml = pastebin.decode_to_xml(pastebin.get_as_xml(key))
                tree = ET.ElementTree(xml)
                tree.write(open(get_test_path(f"in/pastebin_xmls/{PastebinHelper.to_file_name(key)}.xml"), "wb"))

    @staticmethod
    def fetch_pastebin(key: str):
                xml = pastebin.decode_to_xml(pastebin.get_as_xml(key))
                tree = ET.ElementTree(xml)
                file = open(get_test_path(f"in/pastebin_xmls/{PastebinHelper.to_file_name(key)}.xml"), "wb")
                tree.write(file)
                log.debug(f"Wrote content for '{key}'")
                file.close()
