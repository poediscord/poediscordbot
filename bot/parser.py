import logging
from pprint import pprint

from models import Build, Skill, Gem, Item
from util.poeurl import shrink_tree_url


class Parser:
    @staticmethod
    def decode_build(xml_build):
        """
        Decodes all build information and playerstats into the specific model we expect.
        :param xml_build:
        :return:
        """
        build_info = Build(xml_build.attrib['level'], xml_build.attrib['targetVersion'], xml_build.attrib['bandit'],
                           xml_build.attrib['className'],
                           xml_build.attrib['ascendClassName'])
        for player_stat in xml_build:
            build_info.appendStat(player_stat.attrib['stat'], player_stat.attrib['value'])
        return build_info

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

        for skill in xml_skills:
            gems = []
            for gem in skill:
                gems.append(
                    Gem(gem.attrib['nameSpec'], gem.attrib['level'], gem.attrib['quality'], gem.attrib['skillPart'] if 'skillPart' in gem.attrib else None,
                        gem.attrib['enabled']))
            skills.append(Skill(skill.attrib['slot'], gems))

        items = []

        for item in xml_items:
            if item.tag == "Item":
                items.append(Item(item.attrib['id'], item.text))

        build = Build(xml_build.attrib['level'], xml_build.attrib['targetVersion'], xml_build.attrib['bandit'],
                      xml_build.attrib['className'],
                      xml_build.attrib['ascendClassName'], tree, skills, active_skill, items)
        for player_stat in xml_build:
            build.appendStat(player_stat.attrib['stat'], player_stat.attrib['value'])

        return build
