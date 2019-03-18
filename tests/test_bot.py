import unittest

from discord import Embed

from src.bot.discord_bot import parse_pob


def get_links(file="tests/in/pastebins.txt"):
    with open(file,"r") as file:
        return [line.rstrip() for line in file.readlines() if "#" not in line]


class TestBot(unittest.TestCase):
    def test_bot_parse_routine(self):
        """
        Tests whether all links inside of the file can be successfully parsed
        """
        links=get_links()
        for link in links:
            with self.subTest(i=link):
                demo_author = None
                build_embed = parse_pob(demo_author, link)
                self.assertTrue(isinstance(build_embed, Embed))



    def test_illegal_url(self):
        demo_profile_link = 'https://pastebin.com/404URLNOTFOUND'
        demo_author = None
        build_embed = parse_pob(demo_author, demo_profile_link)
        self.assertFalse(isinstance(build_embed, Embed))


if __name__ == '__main__':
    unittest.main()
