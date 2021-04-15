from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.pob_xml_parser.models.gem import Gem
from poediscordbot.pob_xml_parser.models.item_slot import ItemSlot, Item
from poediscordbot.pob_xml_parser.models.skill import Skill
from poediscordbot.pob_xml_parser.tree import poe_tree_codec
from poediscordbot.util.logging import log


def get_attrib_if_exists(xml_elem, key):
    """
    Checks if the attrib key exists and returns either the val or none.
    :param xml_elem: xml element to check
    :param key: key of the attribute
    :return:  vale | none
    """
    return xml_elem.attrib[key] if key in xml_elem.attrib else None


def parse_build(xml_root) -> Build:
    """
    Completely parse the given pob xml into a build.
    :param xml_root: root node of pob xml
    :return: completely parsed build
    """
    xml_build = xml_root.find('Build')
    xml_items = xml_root.find('Items')
    xml_skills = xml_root.find('Skills')
    xml_tree = xml_root.find('Tree')
    selected_tree = _get_tree_link(xml_tree)

    # parse items
    item_slots = _parse_item_slots(xml_items)
    skills = _parse_skills(xml_skills)
    active_skill = get_attrib_if_exists(xml_build, 'mainSocketGroup')

    build = Build(xml_build.attrib['level'], xml_build.attrib['targetVersion'],
                  get_attrib_if_exists(xml_build, 'bandit'),
                  xml_build.attrib['className'],
                  xml_build.attrib['ascendClassName'], selected_tree, skills, active_skill, item_slots)
    for player_stat in xml_build:
        if 'stat' in player_stat.attrib and 'value' in player_stat.attrib:
            build.append_stat(player_stat.attrib['stat'], player_stat.attrib['value'], player_stat.tag)
        else:
            log.info(f"Encountered unsupported player stat: k={player_stat.tag}, v={player_stat.attrib}")

    # parse config
    config = xml_root.find('Config')
    if not config == None:
        for input in xml_root.find('Config'):
            if input.tag == "Input":
                extracted = [val for (key, val) in input.attrib.items()]
                if len(extracted) < 1:
                    continue
                build.append_conf(extracted[0], extracted[1])

    # keystones
    tree = poe_tree_codec.codec.decode_url(selected_tree)
    build.keystones = tree.get_keystones(poe_tree_codec.codec.keystones)
    return build


def _get_tree_link(tree):
    active_spec = get_attrib_if_exists(tree, 'activeSpec')
    tree_index = active_spec if active_spec else 1
    if tree_index:
        # when a tree was selected, get the corresponding url
        selected_tree = tree[int(tree_index) - 1].find('URL').text
        return selected_tree.strip()


def _parse_item_slots(xml_items):
    """
    Parses all entries in the specified xml node depending on the type items or slots are parsed
    :param xml_items: xml node "Items"
    :return: dictionary of item slots [SLOTNAME]:[name, item_id, item]
    """
    items = []
    slots = {}
    active_set = get_attrib_if_exists(xml_items, 'activeItemSet')
    for entry in xml_items:
        # todo: only parse needed items for the current build
        if entry.tag.lower() == "item":
            items.append(
                Item(entry.attrib['id'], entry.text, get_attrib_if_exists(entry, 'variant')))
        # todo: implement check if we need to parse the second weapon set instead of the normal one.
        if entry.tag.lower() == "slot":
            item_id = get_attrib_if_exists(entry, 'itemId')
            item = _parse_item_slot(entry, items, item_id)
            if item:
                slots[entry.attrib['name']] = item

        if entry.tag.lower() == "itemset" and get_attrib_if_exists(entry, 'id') == active_set:
            for slot in entry:
                item_id = get_attrib_if_exists(slot, 'itemId')
                item = _parse_item_slot(slot, items, item_id)
                if item:
                    slots[slot.attrib['name']] = item
    return slots


def _parse_item_slot(entry, items, item_id):
    if item_id:
        # print(item_id)
        # go through all items by their id, if the id matches return the first match of the comprehension.
        item_match = [item for item in items if item.id == item_id]
        item = item_match[0] if len(item_match) > 0 else None
        if item:
            slot = ItemSlot(entry.attrib['name'], item_id, item, get_attrib_if_exists(entry, 'active'))
            return slot


def _parse_skills(xml_skills):
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
            skill_minion_skill = get_attrib_if_exists(gem, 'skillMinionSkill')
            is_minion_skill = True if skill_minion_skill else False
            gems.append(
                Gem(get_attrib_if_exists(gem, 'skillId'), gem.attrib['nameSpec'], gem.attrib['level'],
                    gem.attrib['quality'],
                    get_attrib_if_exists(gem, 'skillPart'),
                    gem.attrib['enabled'],
                    get_attrib_if_exists(gem, 'count'),
                    get_attrib_if_exists(gem, 'skillMinion'),
                    is_minion_skill,
                    get_attrib_if_exists(gem, 'qualityId'),
                    )
            )
        slot = get_attrib_if_exists(skill, 'slot')
        if slot:
            pass
        skills.append(Skill(gems, get_attrib_if_exists(skill, 'mainActiveSkill'), slot, skill.attrib['enabled'],
                            get_attrib_if_exists(skill, 'includeInFullDPS') == 'true'))
    return skills
