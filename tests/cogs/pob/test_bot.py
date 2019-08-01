import unittest

from discord import Embed

from poediscordbot.cogs.pob.pob_cog import PoBCog
from tests import load_file_as_string


def get_links(path="in/pastebins.txt"):
    return [line.rstrip() for line in load_file_as_string(path).split("\n") if "#" not in line]


class TestBot(unittest.TestCase):
    def test_bot_parse_routine(self):
        """
        Tests whether all links inside of the file can be successfully parsed
        """
        links = get_links()
        for link in links:
            with self.subTest(i=link):
                demo_author = None
                build_embed = PoBCog._parse_pob(demo_author, link)
                self.assertTrue(isinstance(build_embed, Embed))

    def test_illegal_url(self):
        demo_profile_link = 'https://pastebin.com/404URLNOTFOUND'
        demo_author = None
        build_embed = PoBCog._parse_pob(demo_author, demo_profile_link)
        self.assertFalse(isinstance(build_embed, Embed))


if __name__ == '__main__':
    unittest.main()
