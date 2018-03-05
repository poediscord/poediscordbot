import logging

from models import Build, Skill, Gem, Item
from util.poeurl import shrink_tree_url


class Parser:
    @staticmethod
    def get_attrib_if_exists(xml_elem, key):
        """
        Checks if the attrib key exists and returns either the val or none.
        :param xml_elem: xml element to check
        :param key: key of the attribute
        :return:  vale | none
        """
        return xml_elem.attrib[key] if key in xml_elem.attrib else None

    @staticmethod
    def parse_build(xml_root):
        xml_build = xml_root.find('Build')
        xml_skills = xml_root.find('Skills')
        xml_items = xml_root.find('Items')
        tree = xml_root.find('Tree').find('Spec').find('URL').text
        try:
            tree = shrink_tree_url(tree)
        except ValueError as err:
            logging.error(err)

        skills = []
        active_skill = xml_build.attrib['mainSocketGroup']

        # parse skills and the supported gems
        for skill in xml_skills:
            gems = []
            for gem in skill:
                gems.append(
                    Gem(Parser.get_attrib_if_exists(gem, 'skillId'), gem.attrib['nameSpec'], gem.attrib['level'],
                        gem.attrib['quality'],
                        Parser.get_attrib_if_exists(gem, 'skillPart'),
                        gem.attrib['enabled']))
            skills.append(Skill(gems, skill.attrib['mainActiveSkill'], Parser.get_attrib_if_exists(skill, 'slot')))

        items = []

        # parse items
        for item in xml_items:
            if item.tag == "Item":
                items.append(Item(item.attrib['id'], item.text))

        build = Build(xml_build.attrib['level'], xml_build.attrib['targetVersion'],
                      Parser.get_attrib_if_exists(xml_build, 'bandit'),
                      xml_build.attrib['className'],
                      xml_build.attrib['ascendClassName'], tree, skills, active_skill, items)
        for player_stat in xml_build:
            build.appendStat(player_stat.attrib['stat'], player_stat.attrib['value'])

        for input in xml_root.find('Config'):
            if input.tag == "Input":
                extracted = [val for (key, val) in input.attrib.items()]
                if len(extracted) < 1:
                    continue
                build.appendConfig(extracted[0], extracted[1])

        return build
