
class PlayerStat:
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def __repr__(self) -> str:
        return "{}".format(self.__dict__)


class Build:
    def __init__(self, level, version, bandit, className, ascendencyName):
        self.level = level
        self.version = version
        self.bandit = bandit
        self.className = className
        self.ascendencyName = ascendencyName
        self.stats = []

    def appendStat(self, stat: PlayerStat):
        self.stats.append(stat)

    def __repr__(self) -> str:
        return "{}".format(self.__dict__)

    def to_string(self):
        ret = ""
        for item in self.__dict__:
            val = self.__dict__[item]
            if isinstance(val, list):
                pass
            else:
                ret += item + ": " + val + "\n"
        return ret
