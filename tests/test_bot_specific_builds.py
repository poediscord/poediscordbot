import json
import unittest
from unittest import mock

from discord import Embed

from src.bot.discord_bot import parse_pob


def get_builds(file="in/specific_builds.json"):
    with open(file, "r") as file:
        return json.loads(file.read())


class TestBot(unittest.TestCase):
    def test_bot_parse_routine(self):
        """
        Tests whether all links inside of the file can be successfully parsed
        """
        demo_author = None

        json = get_builds()
        for build in json['builds']:
            with self.subTest(i=build['name']):
                build_embed = parse_pob(demo_author, build['pastebin'])
                self.assertTrue(isinstance(build_embed, Embed))
                embed_dict = build_embed.to_dict()
                print(embed_dict)
                for assertion in build['assertions']:
                    print(assertion)
                    term, value = assertion['key'], assertion['value']
                    assertion_succeeded = False
                    for field in embed_dict['fields']:
                        if 'level' in term or 'lvl' in term:
                            assertion_succeeded = value in embed_dict.get('title', '')
                        elif 'ascendency' in term:
                            assertion_succeeded = value in embed_dict.get('title', '')
                            assertion_succeeded = assertion_succeeded or value in embed_dict.get('thumbnail', '').get(
                                'url', '')
                        # fixme: remove catchall and precisely go to the section where stuff should be in.
                        elif value in field['value']:
                            assertion_succeeded = True

                        if assertion_succeeded:
                            break
                    self.assertTrue(assertion_succeeded,
                                    msg=f"Assertion ({term}:'{value}') in embed={embed_dict} failed.")


if __name__ == '__main__':
    unittest.main()
