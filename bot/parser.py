import logging

from models import Build, Skill, Gem, Item, ItemSlot
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
        xml_items = xml_root.find('Items')
        xml_skills = xml_root.find('Skills')
        xml_tree = xml_root.find('Tree')
        selected_tree = Parser.get_tree_link(xml_tree)

        # parse items
        item_slots = Parser.parse_item_slots(xml_items)
        skills = Parser.parse_skills(xml_skills)
        active_skill = xml_build.attrib['mainSocketGroup']

        build = Build(xml_build.attrib['level'], xml_build.attrib['targetVersion'],
                      Parser.get_attrib_if_exists(xml_build, 'bandit'),
                      xml_build.attrib['className'],
                      xml_build.attrib['ascendClassName'], selected_tree, skills, active_skill, item_slots)
        for player_stat in xml_build:
            build.append_stat(player_stat.attrib['stat'], player_stat.attrib['value'], player_stat.tag)

        # parse config
        for input in xml_root.find('Config'):
            if input.tag == "Input":
                extracted = [val for (key, val) in input.attrib.items()]
                if len(extracted) < 1:
                    continue
                build.append_conf(extracted[0], extracted[1])

        return build

    @staticmethod
    def get_tree_link(tree):
        tree_index = Parser.get_attrib_if_exists(tree, 'activeSpec')
        if tree_index:
            # when a tree was selected, get the corresponding url
            selected_tree = tree[int(tree_index) - 1].find('URL').text
            try:
                return shrink_tree_url(selected_tree)
            except ValueError as err:
                logging.error("Tree shrinking failed... err={}".format(err))
                return selected_tree

    @staticmethod
    def parse_item_slots(xml_items):
        """
        Parses all entries in the specified xml node depending on the type items or slots are parsed
        :param xml_items: xml node "Items"
        :return: dictionary of item slots [SLOTNAME]:[name, item_id, item]
        """
        items = []
        slots = {}
        for entry in xml_items:
            # todo: only parse needed items for the current build
            if entry.tag.lower() == "item":
                items.append(
                    Item(entry.attrib['id'], entry.text, Parser.get_attrib_if_exists(entry, 'variant')))
            # todo: implement check if we need to parse the second weapon set instead of the normal one.
            if entry.tag.lower() == "slot":
                item_id = Parser.get_attrib_if_exists(entry, 'itemId')
                item = None
                if item_id:
                    item = items[int(item_id) - 1]
                slots[entry.attrib['name']] = ItemSlot(entry.attrib['name'], item_id, item)

        return slots

    @classmethod
    def parse_skills(self, xml_skills):
        """
        Parse all active skill setups from the given xml
        :param xml_skills: root node containing the skills
        :return: list of skills
        """
        skills = []
        # parse skills and the supported gems
        for skill in xml_skills:
            gems = []
            for gem in skill:
                gems.append(
                    Gem(Parser.get_attrib_if_exists(gem, 'skillId'), gem.attrib['nameSpec'], gem.attrib['level'],
                        gem.attrib['quality'],
                        Parser.get_attrib_if_exists(gem, 'skillPart'),
                        gem.attrib['enabled']))
            slot = Parser.get_attrib_if_exists(skill, 'slot')
            if slot:
                pass
            skills.append(Skill(gems, skill.attrib['mainActiveSkill'], slot))
        return skills
