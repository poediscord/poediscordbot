import re

from poediscordbot.cogs.pob.poe_data import poe_consts
from poediscordbot.cogs.pob.util.pob import pob_conf
from poediscordbot.util.logging import log


class Gem:
    __slots__ = 'name', 'level', 'quality', 'id', 'skill_part', 'enabled', 'second_name', 'active_part', 'is_active'

    def __init__(self, gem_id, name, level, quality, skill_part, enabled=''):
        self.name = self.translate_name(gem_id) if name == "" else name
        self.level = int(level)
        self.quality = int(quality)
        self.id = gem_id
        self.skill_part = int(skill_part) if skill_part else None
        self.enabled = True if enabled == 'true' else False
        self.second_name = name.split("Vaal ", 1)
        if len(self.second_name) > 1:
            self.second_name = self.second_name[1]
        else:
            self.second_name = None
        self.active_part = 0
        self.is_active = self.determine_active()

    def __repr__(self) -> str:
        return f"Gem [{self.build_gem_string()}]"

    def determine_active(self):
        return False if not self.id else "Support".lower() not in self.id.lower()

    def get_name(self):
        return self.name if self.active_part == 0 else self.second_name

    def set_active_part(self, part_id):
        self.active_part = part_id

    def build_gem_string(self):
        """
        Get the display string for a gem, adds level and quality info if the gem is remarkable in some way.
        :return: information string: name | name (level/quality)
        """
        exceptional_gems = ['empower', 'enlighten', 'enhance']
        gem_string = self.name

        special_gem = self.name.lower() in exceptional_gems
        high_level = self.level > 20
        is_notable = self.quality > 5

        if special_gem or high_level or is_notable:
            gem_string += f" ({self.level}/{self.quality}%)"
        return gem_string

    def is_valid_gem(self):
        """
        A gem is valid if it's enabled, it has a nonempty, non jewel name
        :return: true if it is a parseable gem
        """
        return self.name and self.enabled and self.name != '' and 'jewel' not in self.name.lower()

    @staticmethod
    def translate_name(skill_id):
        name = None
        if skill_id == 'UniqueAnimateWeapon':
            name = 'Manifest Dancing Dervish'
        if skill_id == 'ChaosDegenAuraUnique':
            name = "Death Aura"
        if skill_id == 'IcestormUniqueStaff12':
            name = "Ice Storm"
        if skill_id == 'TriggeredMoltenStrike':
            name = "Molten Burst"
        if skill_id == 'TriggeredSummonSpider':
            name = "Raise Spiders"
        return name


class Skill:
    def __init__(self, gems, main_active_skill, slot=None, enabled=False):
        self.slot = slot
        self.gems = gems
        self.enabled = True if enabled == 'true' else False
        self.main_active_skill = None

        if main_active_skill and main_active_skill.isdigit():
            self.main_active_skill = int(main_active_skill)

        self.links = len(gems)

    def __repr__(self) -> str:
        return f"Skill [slot={self.slot}; gems={self.gems}; links={self.links}; selected={self.main_active_skill}; " \
            f"enabled={self.enabled}] "

    def get_active_gems(self):
        return [gem for gem in self.gems if gem.is_active]

    def get_selected(self):
        """
        Gets the selected main skill gem. first filter the this gem to only allow supports, then get the right gem
        via the main_active_skill.
        With new Vaal skills: Players can select the non vaal version in index+1 which is not saved in the xml.
        :return:
        """
        gem = None

        if self.main_active_skill:
            active_gems = [gem for gem in self.gems if gem.id and "support" not in gem.id.lower()]
            full_list = []
            # easier abstraction than calculating the stuff
            for gem in active_gems:
                if 'vaal' in gem.name.lower():
                    full_list.append(gem)
                full_list.append(gem)
            if len(full_list) > 1:
                gem = full_list[self.main_active_skill - 1]
                # if the previous gem has the same name, toggle it to be the non val version.
                gem.set_active_part(1 if gem == full_list[self.main_active_skill - 2] else 0)
        return gem

    def get_links(self, item=None, join_str=" + "):
        # Join the gem names, if they are in the selected skill group and if they are enable d. Show quality and level
        # if level is >20 or quality is set.
        ret = join_str.join([gem.build_gem_string() for gem in self.gems if gem.is_valid_gem()])

        if item:
            supports = item.added_supports
            if supports and isinstance(supports, list):
                ret += "\n(+ " + join_str.join([gem['name'] + " (" + gem['level'] + ")" for gem in supports])
                ret += f" from: *{item.name}*)"
        return ret


class ItemSlot:
    def __init__(self, name, item_id, item, active=False):
        self.name = name
        self.item_id = item_id
        self.item = item
        self.active = bool(active)

    def __repr__(self) -> str:
        return f"ItemSlot [name={self.name}; item_id={self.item_id}; item={self.item}; active={self.active}]"


class Item:
    def __init__(self, id, raw_content, variant=None):
        self.id = id
        self.raw_content = raw_content.strip()
        self.variant = variant
        self.name = self.parse_item_name()
        self.added_supports = self.parse_item_for_support()

    def __repr__(self) -> str:
        return f"Item [id={self.id}; name={self.name}; Supports={self.added_supports}]"

    def parse_item_name(self):
        # see here for regex: https://regex101.com/r/MivGPM/1
        regex = r"\s*Rarity:.*\n\s*(.*)\n"
        matches = re.findall(regex, self.raw_content, re.IGNORECASE)
        name = "UNDEFINED"
        try:
            name = matches[0]
        except IndexError as err:
            log.warning(f"Name could not be retrieved. Trying string split method Err={err}")
            name = self.raw_content.split('\n')[0]

        return name

    def parse_item_for_support(self):
        # Socketed Gems are Supported by level 20 Elemental Proliferation
        add_supports = []
        # see here for regex: https://regex101.com/r/CcxRuz/1
        pattern = r"({variant:([0-9,]*)}|)Socketed Gems are Supported by level ([0-9]*) ([a-zA-Z ]*)"
        try:
            supports = re.findall(pattern, self.raw_content, re.IGNORECASE)
            for support in supports:
                # if either no variant exists, or our variant matches the current supports variant
                if 'variant' not in support[0] or self.variant in support[0]:
                    add_supports.append({"name": support[3], "level": support[2]})
        except AttributeError as err:
            return
        return add_supports


class Build:
    def __init__(self, level, version, bandit, class_name, ascendancy_name, tree, skills, active_skill, item_slots):
        self.level = int(level)
        self.version = version
        self.bandit = bandit
        self.class_name = class_name
        self.ascendancy_name = ascendancy_name
        self.stats = {}
        self.config = {}
        self.tree = tree
        self.skills = skills
        self.active_skill_id = int(active_skill) if active_skill else None
        self.item_slots = item_slots
        self.aura_count, self.curse_count = self.count_curses_auras()
        self.keystones = []

    def count_curses_auras(self):
        """
        Iterates through all skills and gems and counts socketed auras and curses
        :return: auracount, curse count as named tuple
        """
        aura_count = 0
        curse_count = 0
        for skill in self.skills:
            if skill.enabled:
                for gem in skill.gems:
                    if gem.enabled:
                        if gem.get_name() in poe_consts.curse_list:
                            curse_count += 1
                        if gem.get_name() in poe_consts.aura_list:
                            aura_count += 1
        return aura_count, curse_count

    def append_stat(self, key, val, stat_owner):
        # remove "Stat" from the string
        stat_owner = stat_owner[:-4]
        if not stat_owner in self.stats:
            self.stats[stat_owner] = {}
        self.stats[stat_owner][key] = float(val)
        # print("owner_key={}; key={}, val={}".format(stat_owner, key, val))

    def append_conf(self, key, val):
        conf_entry = pob_conf.fetch_entry(key)
        # ignore unknown settings.
        if conf_entry:
            self.config[key] = {'value': val}
            self.config[key].update(conf_entry)

    def __repr__(self) -> str:
        return f"{self.__dict__}"

    def get_item(self, slot):
        item_slot = self.item_slots.get(slot)
        if item_slot:
            return item_slot.item

    def get_stat(self, owner, key, threshold=0):
        if owner in self.stats and key in self.stats[owner]:
            val = self.stats[owner][key]
            return val if val >= threshold else None
        else:
            return None

    def to_string(self):
        ret = ""
        for item in self.__dict__:
            val = self.__dict__[item]
            if isinstance(val, list):
                pass
            else:
                ret += item + ": " + val + "\n"
        return ret

    def get_active_skill(self):

        if len(self.skills) < 1 or self.active_skill_id is None or self.active_skill_id < 1:
            return None
        return self.skills[self.active_skill_id - 1]
