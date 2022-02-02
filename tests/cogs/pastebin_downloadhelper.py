import xml.etree.ElementTree as ET

from poediscordbot.cogs.pob.importers import pob_xml_decoder
from poediscordbot.cogs.pob.importers.pastebin import PastebinImporter
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
                xml = pob_xml_decoder.decode_to_xml(PastebinImporter(line).fetch_data(key))
                tree = ET.ElementTree(xml)
                tree.write(open(get_test_path(f"in/pastebin_xmls/{PastebinHelper.to_file_name(key)}.xml"), "wb"))

    @staticmethod
    def fetch_pastebin(key: str):
                xml = pob_xml_decoder.decode_to_xml(PastebinImporter("").fetch_data(key))
                tree = ET.ElementTree(xml)
                file = open(get_test_path(f"in/pastebin_xmls/{PastebinHelper.to_file_name(key)}.xml"), "wb")
                tree.write(file)
                log.debug(f"Wrote content for '{key}'")
                file.close()
