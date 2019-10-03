import unittest

import defusedxml.ElementTree as ET

from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.pob_xml_parser.models.gem import Gem
from poediscordbot.pob_xml_parser.models.skill import Skill
from poediscordbot.pob_xml_parser.pob_xml_parser import parse_build
from tests import load_file_as_string


def load_test_build(path):
    content = load_file_as_string(path)
    xml = ET.fromstring(content)
    return parse_build(xml)


class TestParser(unittest.TestCase):

    def test_juggernaut_tecslam(self):
        build = load_test_build("in/jugg_tectonic.xml")
        # expect to find a tree, ascendancy name, version, level in the build
        self.assertTrue(isinstance(build, Build))
        self.assertTrue(isinstance(build.tree, str))
        self.assertTrue(isinstance(build.ascendancy_name, str))
        self.assertTrue(isinstance(build.version, str))
        self.assertTrue(isinstance(build.level, int))
        expected_tree = "https://www.pathofexile.com/passive-skill-tree" \
                        "/AAAABAEBABzc2WFeE2VNhVLAGgd1WfOPGtI4uUPzjTQxOQ6KIqIAp6XAZkFybyePYKcIBS37i" \
                        "-8Ol3nLHtNvaGXApsbYLPshVT38rY2Yb58-9kgdFMlnvTYUIPAfkn1o8ozPXz" \
                        "-pJ9w9U1IJlq0JBLP463rvh2oWb_PdqW5QR5MH9zJ2rDbpPvEUcb6n2sFAoONqR37" \
                        "cI1hjqZQaOEWdkGxmnoTZLdLqGM9-d-MuU5pqkc4GxiSqu-3BBHlomuByDzLRkFWPRptR5" \
                        "c_60qLqdPFepeRRhO_0g3KpEuEnL7yadO3AAayq6wkTcUVHJyDZfHuMfXNYriFgbzuCB-vuAdw="
        self.assertEqual(expected_tree, build.tree)

        # find the active skill, it must be a skill.
        skill = build.get_active_skill()
        self.assertTrue(isinstance(skill, Skill))
        # selected skill matches
        main_gem = skill.get_selected()
        self.assertTrue(isinstance(main_gem, Gem))
        self.assertEqual("Tectonic Slam", skill.get_selected().get_name())
        self.assertFalse(skill.get_selected().minion_skill)
        self.assertEqual(len(build.item_slots), 14)

    def test_lab_runner(self):
        build = load_test_build("in/pf_labrunner.xml")
        # expect to find a tree, ascendancy name, version, level in the build
        self.assertTrue(isinstance(build, Build))
        self.assertTrue(isinstance(build.tree, str))
        self.assertTrue(isinstance(build.ascendancy_name, str))
        self.assertTrue(isinstance(build.version, str))
        self.assertTrue(isinstance(build.level, int))
        self.assertEqual(build.get_player_stat("EffectiveMovementSpeedMod"), 5.69)
        # find the active skill, it must be a skill.
        skill = build.get_active_skill()
        self.assertTrue(isinstance(skill, Skill))
        # selected skill matches
        main_gem = skill.get_selected()
        self.assertTrue(isinstance(main_gem, Gem))
        self.assertEqual("Blade Vortex", skill.get_selected().get_name())
        self.assertFalse(skill.get_selected().minion_skill)

    def test_minion_skill(self):
        build = load_test_build("in/herald_of_purity_minion.xml")
        # expect to find a tree, ascendancy name, version, level in the build
        self.assertTrue(isinstance(build, Build))
        self.assertTrue(isinstance(build.tree, str))
        self.assertTrue(isinstance(build.ascendancy_name, str))
        self.assertTrue(isinstance(build.version, str))
        self.assertTrue(isinstance(build.level, int))

        skill = build.get_active_skill()
        self.assertTrue(isinstance(skill, Skill))

        main_gem = skill.get_selected()
        self.assertTrue(isinstance(main_gem, Gem))
        self.assertEqual("Herald of Purity", skill.get_selected().get_name())
        self.assertTrue(skill.get_selected().minion_skill)
        self.assertEqual("AxisEliteSoldierHeraldOfLight", skill.get_selected().selected_minion)


if __name__ == '__main__':
    unittest.main()
