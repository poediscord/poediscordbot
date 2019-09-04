import unittest

import defusedxml.ElementTree as ET

from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.pob_xml_parser.models.gem import Gem
from poediscordbot.pob_xml_parser.models.skill import Skill
from poediscordbot.pob_xml_parser.pob_xml_parser import parse_build
from tests import load_file_as_string


def load_test_build(path="in/jugg_tectonic.xml"):
    content = load_file_as_string(path)
    xml = ET.fromstring(content)
    return parse_build(xml)


class TestParser(unittest.TestCase):
    def test_xml_to_build(self):
        build = load_test_build()
        self.assertTrue(isinstance(build.tree, str))
        self.assertTrue(isinstance(build.ascendancy_name, str))
        self.assertTrue(isinstance(build.version, str))
        self.assertTrue(isinstance(build.level, int))

    def test_skills(self):
        build = load_test_build()
        self.assertTrue(isinstance(build, Build))

        skill = build.get_active_skill()
        self.assertTrue(isinstance(skill, Skill))

        main_gem = skill.get_selected()
        self.assertTrue(isinstance(main_gem, Gem))

    def test_item_slots(self):
        build = load_test_build()
        # Test build has exactly 14 equipped items
        self.assertEqual(len(build.item_slots), 14)


if __name__ == '__main__':
    unittest.main()
