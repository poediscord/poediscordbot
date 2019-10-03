import unittest

from discord import Embed

from poediscordbot.cogs.pob.pob_cog import PoBCog
from tests import load_json_file


class TestBot(unittest.TestCase):
    def test_bot_parse_routine(self):
        """
        Tests whether all links inside of the file can be successfully parsed.
        The key in the json has to either be  "level", "ascendency", "skill" or any of the categories in the bot output.
        I.e. "Offense", "Defense", ...
        """
        demo_author = None

        json = load_json_file("in/specific_builds.json")

        for build in json['builds']:
            with self.subTest(i=build['name']):
                build_embed = PoBCog._parse_pob(demo_author, build['pastebin'])
                self.assertTrue(isinstance(build_embed, Embed))
                embed_dict = build_embed.to_dict()
                print(embed_dict)
                for assertion in build['assertions']:
                    print(assertion)
                    key, value, negated = assertion.get('key', ''), assertion.get('value', ''), assertion.get('not',
                                                                                                              False)

                    if key in ['level', 'lvl', 'title']:
                        assertion_succeeded = value in embed_dict.get('title', '')
                        if not negated:
                            self.assertTrue(assertion_succeeded,
                                            msg=f"Assertion ({key}:'{value}') in embed={embed_dict} failed.")
                        else:
                            self.assertFalse(assertion_succeeded,
                                             msg=f"Assertion ({key}:'{value}') in embed={embed_dict} failed.")
                    elif 'ascendency' in key:
                        assertion_succeeded = value in embed_dict.get('title', '')
                        assertion_succeeded = assertion_succeeded or value in embed_dict.get('thumbnail', '').get('url',
                                                                                                                  '')
                        self.assertTrue(assertion_succeeded,
                                        msg=f"Assertion ({key}:'{value}') in embed={embed_dict} failed.")
                    elif 'skill' in key:
                        assertion_succeeded = value in embed_dict.get('title', '')
                        self.assertTrue(assertion_succeeded,
                                        msg=f"Assertion ({key}:'{value}') in embed={embed_dict} failed.")
                    else:
                        for field in embed_dict['fields']:
                            self.single_assert(field, key, value, negated)

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
        print(f"searching embed part={field['name']} for {term},{value} - negated? {negated}")

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
