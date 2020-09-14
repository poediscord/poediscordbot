class JsonifySlotsCls:
    def json(self):
        return {key: getattr(self, key, None) for key in self.__slots__ if getattr(self, key, None) is not None}


class JsonifyBuildSlotsWithConfig:
    def json(self):
        d = {}
        for key in self.__slots__:
            if key == 'config' and getattr(self, key, None) is not None:
                conf_dict = getattr(self, key, None)
                d[key] = [val for val in conf_dict.values()]
            elif key == 'stats' and getattr(self, key, None) is not None:
                stats_dict = getattr(self, key, None)
                d[key] = [self.unpack_stat(key, val) for val in stats_dict.values()]
            elif getattr(self, key, None) is not None:
                d[key] = getattr(self, key, None)
        return d

    @staticmethod
    def unpack_stat(owner: str, stat: {}):
        print(f">> {stat}")
        stats = []
        for key, value in stat.items():
            stats.append({'owner': owner, 'name': key, 'value': value})
        return stats
