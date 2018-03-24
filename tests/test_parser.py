import unittest
import defusedxml.ElementTree as ET
from bot.pob_parser import parse_build
from models import Build, Skill, Gem


def load_test_build(file='in/jugg_tectonic.xml'):
    xml_str = open(file).read()
    xml = ET.fromstring(xml_str)
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
        self.assertEquals(len(build.item_slots),14)



if __name__ == '__main__':
    unittest.main()
