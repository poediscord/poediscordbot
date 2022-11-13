import os
import unittest
from unittest.mock import patch

import defusedxml.ElementTree as ET
from discord import Embed
from instance import config

from poediscordbot.cogs.pob.importers import PasteData
from poediscordbot.cogs.pob.pob_cog import PoBCog
from poediscordbot.util.logging import log
from tests import load_file_as_string, get_test_path
from tests.cogs import file_loader
from tests.cogs.pastebin_downloadhelper import PastebinHelper


def get_links(path="in/pastebins.txt"):
    return [line.rstrip() for line in load_file_as_string(path).split("\n") if "#" not in line]


class TestBot(unittest.TestCase):
    @staticmethod
    def conf_disable_tree_renderer():
        # return config.ROOT_DIR, config.render_tree_image, config.tree_image_delete_threshold_seconds, config.tree_image_dir
        return config.ROOT_DIR, False, 60 * 10, ''

    @patch.object(PoBCog, 'cleanup_imgs')
    def test_tree_renderer_setup(self, mock):
        paste_key = "0AHp5hgd"
        xml_tree = file_loader.load_xml_by_pastebin_key(paste_key)
        demo_author = None
        data = PasteData(paste_key, f"https://pastebin.com/{paste_key}", "pastebin")

        build_embed, _ = PoBCog(None, [], True)._generate_embed(data, xml_tree, demo_author)
        self.assertTrue(isinstance(build_embed, Embed))
        # ensure self cleaning is triggered on creation
        self.assertTrue(mock.start.called)

    @patch.object(PoBCog, 'read_conf', conf_disable_tree_renderer)
    def test_bot_parse_routine(self):
        """
        Tests whether all links inside of the file can be successfully parsed
        """
        links = get_links()
        xml_keys = file_loader.get_pastebin_keys()

        for link in links:
            if "https://pastebin.com/" in link:
                key = link.split("/")[-1]
                if key not in xml_keys:
                    log.warning(f"Downloading xml from pastebin for key={key}")
                    PastebinHelper.fetch_pastebin(key)

        xml_file_paths = file_loader.get_pastebin_file_dir_files()
        for file_path in xml_file_paths:
            test_path = get_test_path(os.path.join(file_loader.pastebin_xmls_file, file_path))
            with open(test_path, "r") as f:
                demo_author = None
                log.info(f"Testing whether we can parse '{test_path}'")
                xml_tree = ET.fromstring(f.read())

                paste_key = file_path.split('.xml')[0]
                data = PasteData(paste_key, f"https://pastebin.com/{paste_key}", "pastebin")

                build_embed, _ = PoBCog(None, [], True)._generate_embed(data, xml_tree, demo_author)
                self.assertTrue(isinstance(build_embed, Embed))

    @patch.object(PoBCog, 'read_conf', conf_disable_tree_renderer)
    def test_illegal_url(self):
        paste_key = '404URLNOTFOUND'
        demo_author = None
        data = PasteData(paste_key, f"https://pastebin.com/{paste_key}", "pastebin")
        build_embed = PoBCog(None, [], True)._generate_embed(data, None, demo_author)
        self.assertFalse(isinstance(build_embed, Embed))

    @patch.object(PoBCog, 'read_conf', conf_disable_tree_renderer)
    def test_empty_embed_field(self):
        """
        Empty names or values should not be carried into the embed. The pastebin has no secondary defense value
        :return:
        """
        demo_profile_link = 'https://pastebin.com/X8XNW4EU'
        demo_author = None
        xml, data = PoBCog._fetch_xml(demo_author, demo_profile_link)
        build_embed, _ = PoBCog(None, [], True)._generate_embed(data, xml, demo_author, minify=True)

        self.assertTrue(isinstance(build_embed, Embed))
        fields = build_embed._fields
        for field in fields:
            self.assertIsNotNone(field['name'])
            self.assertIsNotNone(field['value'])

        self.assertEqual([], [field['name'] for field in fields if "Secondary Defense" in field['name']],
                         "Build should not have secondary defense field in embed")


if __name__ == '__main__':
    unittest.main()
