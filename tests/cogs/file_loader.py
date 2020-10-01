import os
from typing import List

from tests import get_test_path

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