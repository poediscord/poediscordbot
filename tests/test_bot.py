import unittest

from discord import Embed

import config
from bot.discord_bot import parse_pob
from util.logging import log


class TestParser(unittest.TestCase):
    def test_bot_parse_routine(self):
        demo_profile_link = 'https://pastebin.com/WrXqkFqW'
        print(config.ROOT_DIR)
        demo_author = None
        build_embed = parse_pob(demo_author, demo_profile_link)
        self.assertTrue(isinstance(build_embed, Embed))

    def test_illegal_url(self):
        demo_profile_link = 'https://pastebin.com/404URLNOTFOUND'
        demo_author = None
        build_embed = parse_pob(demo_author, demo_profile_link)
        self.assertEquals(build_embed, None)

if __name__ == '__main__':
    unittest.main()
