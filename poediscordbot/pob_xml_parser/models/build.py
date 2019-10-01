from enum import Enum

from poediscordbot.cogs.pob.poe_data import poe_consts
from poediscordbot.cogs.pob.util.pob import pob_conf


class StatOwner(Enum):
    """
    An enum that represent possible stat owners, currently this is only used for player stats
    """
    PLAYER = "Player"

    @staticmethod
    def from_string(stat_owner):
        if StatOwner.PLAYER.value in stat_owner:
            return StatOwner.PLAYER


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
        stat_owner = StatOwner.from_string(stat_owner)
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

    def _get_stat(self, owner: StatOwner, key, threshold=0):
        if owner in self.stats and key in self.stats[owner]:
            val = self.stats[owner][key]
            return val if val >= threshold \
                else None
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

    def get_player_stat(self, stat_name, threshold=0):
        """
        Wrapper method for the internal get stat method, that only reads player stats
        :param stat_name: name of the stat in Pob XMLs such as "Str", "Int", ...
        :param threshold: optional threshold which is the comparison base for this stat
        :return: value if found (and above threshold) else None
        """
        return self._get_stat(StatOwner.PLAYER, stat_name, threshold=threshold)
