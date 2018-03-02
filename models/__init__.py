class Gem:
    def __init__(self, name, level, quality, skill_part, enabled=''):
        self.name = name
        self.level = level
        self.quality = quality
        self.skill_part = skill_part
        self.enabled = True if enabled == 'true' else False

    def __repr__(self) -> str:
        return "Gem [name={}]".format(self.name)


class Skill:
    def __init__(self, slot, gems):
        self.slot = slot
        self.gems = gems
        self.links = len(gems)

    def __repr__(self) -> str:
        return "Skill [slot={}; gems={} links={}]".format(self.slot, self.gems, self.links)


class Item:
    def __init__(self, id, raw_content):
        self.id = id
        self.raw_content = raw_content.strip()

    def __repr__(self) -> str:
        return "Item [id={}; raw={}]".format(self.id, self.raw_content[:50])


class Build:
    def __init__(self, level, version, bandit, class_name, ascendency_name, tree, skills, activeSkill, items):
        self.level = level
        self.version = version
        self.bandit = bandit
        self.class_name = class_name
        self.ascendency_name = ascendency_name
        self.stats = {}
        self.tree = tree
        self.skills = skills
        self.activeSkill = activeSkill
        self.items = items

    def appendStat(self, key, val):
        self.stats[key] = val

    def __repr__(self) -> str:
        return "{}".format(self.__dict__)

    def get_string(self, keys):
        ret = ""
        for key in keys:
            if key in self.__dict__:
                val = self.__dict__[key]
                if not isinstance(val, list) and val != "None":
                    ret += key + ": " + val + "\n"
        return ret

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
        return self.skills[int(self.activeSkill)-1]

