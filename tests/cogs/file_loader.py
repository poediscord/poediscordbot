import os
from typing import List

import defusedxml.ElementTree as ET

from poediscordbot.util.logging import log
from tests import get_test_path
from tests.cogs.pastebin_downloadhelper import PastebinHelper

pastebin_xmls_file = "in/pastebin_xmls"


def get_pastebin_keys() -> List[str]:
    return [xml.split(".xml")[0] for xml in get_pastebin_file_dir_files()]


def get_pastebin_file_dir_files() -> List[str]:
    return get_files_in_directory(pastebin_xmls_file)


def get_files_in_directory(path) -> List[str]:
    path = get_test_path(path)
    xml_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.xml')]
    return xml_files


def get_pastebin_file(paste_key_filename):
    base_path = get_test_path(pastebin_xmls_file)
    return os.path.join(base_path, paste_key_filename)


def load_xml_by_pastebin_key(pastebin_url) -> ET:
    key = pastebin_url.split("/")[-1]
    xml_keys = get_pastebin_keys()

    if key not in xml_keys:
        log.warning(f"Downloading xml from pastebin for key={key}")
        PastebinHelper.fetch_pastebin(key)

    matches = [file for file in get_pastebin_file_dir_files() if key in file]
    build_xml_file = matches[0] if len(matches) > 0 else None
    path_to_build_xml = get_pastebin_file(build_xml_file)
    with open(path_to_build_xml, "r") as f:
        demo_author = None
        log.info(f"Testing whether we can parse '{build_xml_file}'")

        xml_tree = ET.fromstring(f.read())
    return xml_tree
