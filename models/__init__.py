import logging


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
    def __init__(self, gems, main_active_skill, slot="not specified"):
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

    def get_links(self, join_str=" + "):
        # Join the gem names, if they are in the slected skill group and if they are enabled
        ret = join_str.join([gem.name for gem in self.gems if gem.enabled == True])
        if ret == "":
            ret = None
        return ret


class Item:
    def __init__(self, id, raw_content):
        self.id = id
        self.raw_content = raw_content.strip()

    def __repr__(self) -> str:
        return "Item [id={}; raw={}]".format(self.id, self.raw_content[:50].replace('\n', ' '))


class Build:
    def __init__(self, level, version, bandit, class_name, ascendency_name, tree, skills, activeSkill, items):
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
        self.items = items

    def appendStat(self, key, val):
        self.stats[key] = float(val)

    def appendConfig(self, key, val):
        self.config[key] = val

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
        return self.skills[self.activeSkill - 1]
