import unittest

import defusedxml.ElementTree as ET
from src.bot.pob_parser import parse_build

from src.models import Build, Skill, Gem


def load_test_build(file='tests/in/jugg_tectonic.xml'):
    with open(file, 'r') as f:
        xml = ET.fromstring(f.read())
        parse_build(xml)
        return parse_build(xml)


class TestParser(unittest.TestCase):
    def test_xml_to_build(self):
        build = load_test_build()
        self.assertTrue(isinstance(build.tree,str))
        self.assertTrue(isinstance(build.ascendency_name,str))
        self.assertTrue(isinstance(build.version,str))
        self.assertTrue(isinstance(build.level,int))


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
        self.assertEqual(len(build.item_slots),14)



if __name__ == '__main__':
    unittest.main()
