import json
import os

import defusedxml.ElementTree as ET

from poediscordbot.cogs.pob.importers import pob_xml_decoder
from poediscordbot.pob_xml_parser.pob_xml_parser import parse_build

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def load_file_as_string(path):
    with open(TEST_DIR + os.sep + path, "r") as file:
        return file.read()


def load_json_file(path):
    return json.loads(load_file_as_string(path))


def get_test_path(file):
    return os.path.join(TEST_DIR, file)


def load_test_build(path):
    content = load_file_as_string(path)
    content = pob_xml_decoder.xml_byte_to_str(content)
    xml = ET.fromstring(content)
    return parse_build(xml)