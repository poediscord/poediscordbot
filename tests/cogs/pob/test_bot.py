import os
import unittest

import defusedxml.ElementTree as ET
from discord import Embed

from poediscordbot.cogs.pob.pob_cog import PoBCog
from poediscordbot.util.logging import log
from tests import load_file_as_string, get_test_path
from tests.cogs.pastebin_downloadhelper import PastebinHelper


def get_links(path="in/pastebins.txt"):
    return [line.rstrip() for line in load_file_as_string(path).split("\n") if "#" not in line]


def get_files_in_directory(path):
    path = get_test_path(path)
    xml_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.xml')]
    return xml_files


class TestBot(unittest.TestCase):
    def test_bot_parse_routine(self):
        """
        Tests whether all links inside of the file can be successfully parsed
        """
        folder_path = "in/pastebin_xmls"
        xml_file_paths = get_files_in_directory(folder_path)
        links = get_links()
        xml_keys = [xml.split(".xml")[0] for xml in xml_file_paths]

        for link in links:
            if link.startswith("pastebin"):
                key = link.split("/")[-1]
                if key not in xml_keys:
                    log.warning(f"Downloading xml from pastebin for key={key}")
                    PastebinHelper.fetch_pastebin(key)

        for file_path in xml_file_paths:
            test_path = get_test_path(os.path.join(folder_path, file_path))
            with open(test_path, "r") as f:
                demo_author = None
                log.info(f"Testing whether we can parse '{test_path}'")
                # element tree = xyz
                xml_tree = ET.fromstring(f.read())

                build_embed = PoBCog._generate_embed(None, xml_tree, demo_author,
                                                     f"https://pastebin.com/{file_path.split('.xml')[0]}")
                self.assertTrue(isinstance(build_embed, Embed))

    def test_illegal_url(self):
        demo_profile_link = 'https://pastebin.com/404URLNOTFOUND'
        demo_author = None
        build_embed = PoBCog._generate_embed(None, None, demo_author, demo_profile_link)
        self.assertFalse(isinstance(build_embed, Embed))

    def test_empty_embed_field(self):
        """
        Empty names or values should not be carried into the embed. The pastebin has no secondary defense value
        :return:
        """
        demo_profile_link = 'https://pastebin.com/X8XNW4EU'
        demo_author = None
        xml, web_poe_token, paste_key = PoBCog._fetch_xml(demo_author, demo_profile_link)
        if xml and web_poe_token:
            build_embed = PoBCog._generate_embed(web_poe_token, xml, demo_author,paste_key, minify=True)

        self.assertTrue(isinstance(build_embed, Embed))
        fields = build_embed._fields
        for field in fields:
            self.assertIsNotNone(field['name'])
            self.assertIsNotNone(field['value'])

        self.assertEqual([], [field['name'] for field in fields if "Secondary Defense" in field['name']],
                         "Build should not have secondary defense field in embed")


if __name__ == '__main__':
    unittest.main()
