import json
import unittest

from discord import Embed

from src.bot.discord_bot import parse_pob


def get_builds(file="tests/in/specific_builds.json"):
    with open(file, "r") as file:
        return json.loads(file.read())



class TestBot(unittest.TestCase):
    def test_bot_parse_routine(self):
        """
        Tests whether all links inside of the file can be successfully parsed.
        The key in the json has to either be  "level", "ascendency", "skill" or any of the categories in the bot output.
        I.e. "Offense", "Defense", ...
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
                    term, value, negated = assertion.get('key', ''), assertion.get('value', ''), assertion.get('not',
                                                                                                               False)

                    if 'level' in term or 'lvl' in term:
                        assertion_succeeded = value in embed_dict.get('title', '')
                        self.assertTrue(assertion_succeeded,
                                        msg=f"Assertion ({term}:'{value}') in embed={embed_dict} failed.")
                    elif 'ascendency' in term:
                        assertion_succeeded = value in embed_dict.get('title', '')
                        assertion_succeeded = assertion_succeeded or value in embed_dict.get('thumbnail', '').get('url',
                                                                                                                  '')
                        self.assertTrue(assertion_succeeded,
                                        msg=f"Assertion ({term}:'{value}') in embed={embed_dict} failed.")
                    elif 'skill' in term:
                        assertion_succeeded = value in embed_dict.get('title', '')
                        self.assertTrue(assertion_succeeded,
                                        msg=f"Assertion ({term}:'{value}') in embed={embed_dict} failed.")
                    else:
                        assertion_succeeded = False
                        for field in embed_dict['fields']:
                            assertion_succeeded = self.single_assert(field, term, value, negated)
                            if assertion_succeeded:
                                break

    def single_assert(self, field, term, value, negated):
        """
        Assert that the term, value and whether the term is negated apply to the given field.
        :param field: embed field to search
        :param term: term we search for
        :param value: we want to match
        :param negated: negated
        :return:  true if the assertion succeeded
        """
        do_check = term in field['name']
        print(f"searching title={field['name']}for {term},{value} - negated? {negated}")

        if do_check:
            print(f"searching for {term},{value} - negated? {negated}")
            if not negated:
                self.assertTrue(value in field['value'],
                                msg=f"Assertion ({term}:'{value}') in embed failed.")
            elif negated:
                self.assertTrue(value not in field['value'],
                                msg=f"Assertion ({term}:'{value}') not in embed failed.")


if __name__ == '__main__':
    unittest.main()
