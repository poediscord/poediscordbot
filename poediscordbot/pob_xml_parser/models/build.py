from enum import Enum
from functools import reduce
from typing import Optional

from poediscordbot.cogs.pob.poe_data import poe_consts
from poediscordbot.cogs.pob.util.pob import pob_conf
from poediscordbot.pob_xml_parser.models.skill import Skill
from poediscordbot.util.logging import log


class StatOwner(Enum):
    """
    An enum that represent possible stat owners, currently this is only used for player stats
    """
    PLAYER = "Player"
    MINION = "Minion"

    @staticmethod
    def from_string(stat_owner):
        if StatOwner.PLAYER.value in stat_owner:
            return StatOwner.PLAYER
        if StatOwner.MINION.value in stat_owner:
            return StatOwner.MINION


class Build:
    __slots__ = 'level', 'version', 'bandit', 'class_name', 'ascendancy_name', 'stats', 'config', 'tree', 'skills', \
                'active_skill_id', 'item_slots', 'aura_count', 'curse_count', 'keystones'

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
        stat_owner = StatOwner.from_string(stat_owner)
        if not stat_owner in self.stats:
            self.stats[stat_owner] = {}
        try:
            self.stats[stat_owner][key] = float(val)
        except ValueError:
            log.info(f"Unable to convert '{key}'='{val}' to float.")

    def append_conf(self, key, val):
        conf_entry = pob_conf.fetch_config_entry(key)
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

    def _get_stat(self, owner: StatOwner, key, threshold=0, default_val=None):
        if owner in self.stats and key in self.stats[owner]:
            val = self.stats[owner][key]
            return val if val >= threshold \
                else default_val
        else:
            return default_val

    def to_string(self):
        ret = ""
        for item in self.__dict__:
            val = self.__dict__[item]
            if isinstance(val, list):
                pass
            else:
                ret += item + ": " + val + "\n"
        return ret

    def get_active_skill(self) -> Optional[Skill]:
        if len(self.skills) < 1 or self.active_skill_id is None or self.active_skill_id < 1:
            return None
        return self.skills[self.active_skill_id - 1]

    def get_active_gem_from_included_skills(self) -> [Skill]:
        """
        get all active gems that are included in full dps breakdown with a count above 0
        :return: list of matching gems
        """
        included_skills = [skill.get_active_gems() for skill in self.skills if skill.included_in_full_dps]
        flatmap_included_skills = reduce(lambda a, b: a + b, included_skills) if included_skills else []
        return [gem for gem in flatmap_included_skills if gem.is_active and gem.instance_count > 0]

    def get_player_stat(self, stat_name, threshold=0, default_val=None):
        """
        Wrapper method for the internal get stat method, that only reads player stats
        :param stat_name: name of the stat in Pob XMLs such as "Str", "Int", ...
        :param threshold: optional threshold which is the comparison base for this stat
        :return: value if found (and above threshold) else None
        """
        return self._get_stat(StatOwner.PLAYER, stat_name, threshold=threshold, default_val=default_val)

    def get_minion_stat(self, stat_name, threshold=0, default_val=None):
        return self._get_stat(StatOwner.MINION, stat_name, threshold=threshold, default_val=default_val)
