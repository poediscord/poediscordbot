import unittest

from discord import Embed

from poediscordbot.cogs.pob.output import pob_output
from poediscordbot.cogs.pob.pob_cog import PoBCog
from poediscordbot.cogs.pob.poe_data import poe_consts
from poediscordbot.cogs.pob.util import pastebin
from poediscordbot.pob_xml_parser import pob_xml_parser
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

        for json_build in json['builds']:
            with self.subTest(i=json_build['name']):
                # load data from pastebin if needed
                if 'data' not in json_build:
                    build_embed = PoBCog._parse_pob(demo_author, json_build['pastebin'])
                # load data locally from the 'data' value
                else:
                    xml = pastebin.decode_to_xml(json_build['data'])
                    build = pob_xml_parser.parse_build(xml)
                    build_embed = pob_output.generate_response(demo_author, build, minified=False, pastebin_key=None,
                                                               non_dps_skills=poe_consts, web_poe_token=None)

                self.assertTrue(isinstance(build_embed, Embed))
                embed_dict = build_embed.to_dict()
                print(embed_dict)
                for assertion in json_build['assertions']:
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
                    elif 'ascendancy' in key:
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
