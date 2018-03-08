import logging

import re


class Gem:
    def __init__(self, id, name, level, quality, skill_part, enabled=''):
        self.name = name
        self.level = level
        self.quality = quality
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
            active_skills = [gem for gem in self.gems if "support" not in gem.id.lower()]
            # print(active_skills)
            return active_skills[self.main_active_skill - 1]
        return None

    def get_links(self, item=None, join_str=" + "):
        # Join the gem names, if they are in the slected skill group and if they are enabled
        ret = join_str.join(
            [gem.name + " [L" + gem.level + "|Q" + gem.quality + "]" for gem in self.gems if gem.enabled == True])
        if item:
            supports = item.added_supports
            if supports and isinstance(supports, list):
                ret += "\n(+ " + join_str.join([gem['name'] + " [L" + gem['level'] + "|Q0]" for gem in supports])
                ret += "; From: {})".format(item.name)
        return ret


class ItemSlot:
    def __init__(self, name, item_id, item):
        self.name = name
        self.item_id = item_id
        self.item = item

    def __repr__(self) -> str:
        return "ItemSlot [name={}; item_id={}; item={}]".format(self.name, self.item_id, self.item)


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
        return matches[0]

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
        self.level = level
        self.version = version
        self.bandit = bandit
        self.class_name = class_name
        self.ascendency_name = ascendency_name
        self.stats = {}
        self.config = {}
        self.tree = tree
        self.skills = skills
        self.activeSkill = int(activeSkill)
        self.item_slots = item_slots

    def appendStat(self, key, val, stat_owner):
        # remove "Stat" from the string
        stat_owner = stat_owner[:-4]
        if not stat_owner in self.stats:
            self.stats[stat_owner] = {}
        self.stats[stat_owner][key] = float(val)
        print("owner_key={}; key={}, val={}".format(stat_owner, key, val))

    def appendConfig(self, key, val):
        self.config[key] = val

    def __repr__(self) -> str:
        return "{}".format(self.__dict__)

    def get_item(self, slot):
        return self.item_slots[slot].item

    def get_stat(self, key):
        if key in self.stats:
            return self.stats[key]
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
        if self.activeSkill < 1:
            return None
        return self.skills[self.activeSkill - 1]
