from models import Skill, Item, Build, ItemSlot, Gem
from util.logging import log
from util.poeurl import shrink_tree_url


def get_attrib_if_exists(xml_elem, key):
    """
    Checks if the attrib key exists and returns either the val or none.
    :param xml_elem: xml element to check
    :param key: key of the attribute
    :return:  vale | none
    """
    return xml_elem.attrib[key] if key in xml_elem.attrib else None


def parse_build(xml_root):
    xml_build = xml_root.find('Build')
    xml_items = xml_root.find('Items')
    xml_skills = xml_root.find('Skills')
    xml_tree = xml_root.find('Tree')
    selected_tree = get_tree_link(xml_tree)

    # parse items
    item_slots = parse_item_slots(xml_items)
    skills = parse_skills(xml_skills)
    active_skill = xml_build.attrib['mainSocketGroup']

    build = Build(xml_build.attrib['level'], xml_build.attrib['targetVersion'],
                  get_attrib_if_exists(xml_build, 'bandit'),
                  xml_build.attrib['className'],
                  xml_build.attrib['ascendClassName'], selected_tree, skills, active_skill, item_slots)
    for player_stat in xml_build:
        if 'stat' in player_stat.attrib and 'value' in player_stat.attrib:
            build.append_stat(player_stat.attrib['stat'], player_stat.attrib['value'], player_stat.tag)
        else:
            log.info("Encountered unsupported player stat: k={}, v={}".format(player_stat.tag, player_stat.attrib))

    # parse config
    for input in xml_root.find('Config'):
        if input.tag == "Input":
            extracted = [val for (key, val) in input.attrib.items()]
            if len(extracted) < 1:
                continue
            build.append_conf(extracted[0], extracted[1])

    return build


def get_tree_link(tree):
    tree_index = get_attrib_if_exists(tree, 'activeSpec')
    if tree_index:
        # when a tree was selected, get the corresponding url
        selected_tree = tree[int(tree_index) - 1].find('URL').text
        try:
            return shrink_tree_url(selected_tree)
        except ValueError as err:
            log.error("Tree shrinking failed... err={}".format(err))
            return selected_tree


def parse_item_slots(xml_items):
    """
    Parses all entries in the specified xml node depending on the type items or slots are parsed
    :param xml_items: xml node "Items"
    :return: dictionary of item slots [SLOTNAME]:[name, item_id, item]
    """
    items = []
    slots = {}
    activeSet = get_attrib_if_exists(xml_items, 'activeItemSet')
    for entry in xml_items:
        # todo: only parse needed items for the current build
        if entry.tag.lower() == "item":
            items.append(
                Item(entry.attrib['id'], entry.text, get_attrib_if_exists(entry, 'variant')))
        # todo: implement check if we need to parse the second weapon set instead of the normal one.
        if entry.tag.lower() == "slot":
            item_id = get_attrib_if_exists(entry, 'itemId')
            item = parse_item_slot(entry, items, item_id)
            if item:
                slots[entry.attrib['name']] = item

        if entry.tag.lower() == "itemset" and get_attrib_if_exists(entry, 'id') == activeSet:
            for slot in entry:
                item_id = get_attrib_if_exists(slot, 'itemId')
                item = parse_item_slot(slot, items, item_id)
                if item:
                    slots[slot.attrib['name']] = item
    return slots


def parse_item_slot(entry, items, item_id):
    if item_id:
        # print(item_id)
        # go through all items by their id, if the id matches return the first match of the comprehension.
        item_match = [item for item in items if item.id == item_id]
        item = item_match[0] if len(item_match)>0 else None
        if item:
            slot = ItemSlot(entry.attrib['name'], item_id, item, get_attrib_if_exists(entry, 'active'))
            return slot


def parse_skills(xml_skills):
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
                Gem(get_attrib_if_exists(gem, 'skillId'), gem.attrib['nameSpec'], gem.attrib['level'],
                    gem.attrib['quality'],
                    get_attrib_if_exists(gem, 'skillPart'),
                    gem.attrib['enabled']))
        slot = get_attrib_if_exists(skill, 'slot')
        if slot:
            pass
        skills.append(Skill(gems, skill.attrib['mainActiveSkill'], slot))
    return skills
