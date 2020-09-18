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
                stats_list = []
                for owner in stats_dict:
                    stats_list += [{'owner': owner, 'name': key, 'value': value} for key, value in
                                   stats_dict[owner].items()]
                d[key] = stats_list
            elif getattr(self, key, None) is not None:
                d[key] = getattr(self, key, None)
        return d
