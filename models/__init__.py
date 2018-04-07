import re

from util.logging import log
from util.pob import pob_conf


class Gem:
    def __init__(self, id, name, level, quality, skill_part, enabled=''):
        self.name = name
        self.level = int(level)
        self.quality = int(quality)
        self.id = id
        self.skill_part = int(skill_part) if skill_part else None
        self.enabled = True if enabled == 'true' else False

    def __repr__(self) -> str:
        return "Gem [name={}]".format(self.name)


class Skill:
    def __init__(self, gems, main_active_skill, slot=None):
        self.slot = slot
        self.gems = gems
        try:
            self.main_active_skill = int(main_active_skill)
        except:
            self.main_active_skill = None
        self.links = len(gems)

    def __repr__(self) -> str:
        return "Skill [slot={}; gems={}; links={}; selected={}]".format(self.slot, self.gems, self.links,
                                                                        self.main_active_skill)

    def get_selected(self):
        if self.main_active_skill:
            active_skills = [gem for gem in self.gems if  gem.id and  "support" not in gem.id.lower()]
            # print(active_skills)
            return active_skills[self.main_active_skill - 1]
        return None

    def get_links(self, item=None, join_str=" + "):
        # Join the gem names, if they are in the slected skill group and if they are enabled. Show quality and level if level is >20 or quality is set.
        ret = join_str.join(
            [gem.name + " ({}/{})".format(gem.level, gem.quality) if (gem.level > 20 or gem.quality > 0)
             else gem.name for gem in self.gems if gem.enabled == True and 'jewel' not in gem.name.lower()])
        if item:
            supports = item.added_supports
            if supports and isinstance(supports, list):
                ret += "\n(+ " + join_str.join([gem['name'] + " (" + gem['level'] + ")" for gem in supports])
                ret += " from: *{}*)".format(item.name)
        return ret


class ItemSlot:
    def __init__(self, name, item_id, item, active=False):
        self.name = name
        self.item_id = item_id
        self.item = item
        self.active = bool(active)

    def __repr__(self) -> str:
        return "ItemSlot [name={}; item_id={}; item={}; active={}]".format(self.name, self.item_id, self.item,
                                                                           self.active)


class Item:
    def __init__(self, id, raw_content, variant=None):
        self.id = id
        self.raw_content = raw_content.strip()
        self.variant = variant
        self.name = self.parse_item_name()
        self.added_supports = self.parse_item_for_support()

    def __repr__(self) -> str:
        return "Item [id={}; name={}; Supports={}]".format(self.id, self.name, self.added_supports)

    def parse_item_name(self):
        # see here for regex: https://regex101.com/r/MivGPM/1
        regex = r"\s*Rarity:.*\n\s*(.*)\n"
        matches = re.findall(regex, self.raw_content, re.IGNORECASE)
        name = "UNDEFINED"
        try:
            name = matches[0]
        except IndexError as err:
            log.warning("Name could not be retrieved. Trying string split method Err={}".format(err))
            name = self.raw_content.split('\n')[0]

        return name

    def parse_item_for_support(self):
        # Socketed Gems are Supported by level 20 Elemental Proliferation
        add_supports = []
        # see here for regex: https://regex101.com/r/CcxRuz/1
        regex = r"({variant:([0-9,]*)}|)Socketed Gems are Supported by level ([0-9]*) ([a-zA-Z ]*)"
        try:
            supports = re.findall(regex, self.raw_content, re.IGNORECASE)
            for support in supports:
                # if either no variant exists, or our variant matches the current supports variant
                if 'variant' not in support[0] or self.variant in support[0]:
                    add_supports.append({"name": support[3], "level": support[2]})
        except AttributeError as err:
            return
        return add_supports


class Build:
    def __init__(self, level, version, bandit, class_name, ascendency_name, tree, skills, activeSkill, item_slots):
        self.level = int(level)
        self.version = version
        self.bandit = bandit
        self.class_name = class_name
        self.ascendency_name = ascendency_name
        self.stats = {}
        self.config = {}
        self.tree = tree
        self.skills = skills
        self.active_skill_id = int(activeSkill)
        self.item_slots = item_slots

    def append_stat(self, key, val, stat_owner):
        # remove "Stat" from the string
        stat_owner = stat_owner[:-4]
        if not stat_owner in self.stats:
            self.stats[stat_owner] = {}
        self.stats[stat_owner][key] = float(val)
        # print("owner_key={}; key={}, val={}".format(stat_owner, key, val))

    def append_conf(self, key, val):
        conf_enry = pob_conf.fetch_entry(key)
        # ignore unknown settings.
        if conf_enry:
            self.config[key] = {'value': val}
            self.config[key].update(conf_enry)

    def __repr__(self) -> str:
        return "{}".format(self.__dict__)

    def get_item(self, slot):
        if slot:
            return self.item_slots[slot].item

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
        if len(self.skills) < 1 or self.active_skill_id < 1:
            return None
        return self.skills[self.active_skill_id - 1]
