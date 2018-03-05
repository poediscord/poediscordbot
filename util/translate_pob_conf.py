import logging
import json


class PobConfig():
    def __init__(self, path_to_pob_config="pob_conf.json"):
        self.config = json.load(open(path_to_pob_config))


    def pob_find_entry(self, config_var: str, version="3_0"):
        """
        Reads the pob_config.json and finds the specific entries that are needed.
        :param config_var:
        :param version:
        :return:
        """
        for entry in self.config['conf']:
            if 'var' in entry and entry['var'] == config_var and (
                            'ifVer' not in entry or entry['ifVer'] == version):
                return entry


    def pob_find_all(self, config_vars: [str], version="3_0"):
        """
        Reads the pob_config.json and finds the specific entries that are needed.
        :param config_var:
        :param version:
        :return:
        """
        ret = []

        for entry in self.config['conf']:
            if 'var' in entry and entry['var'] in config_vars:
                if 'ifVer' not in entry or entry['ifVer'] == version:
                    ret.append(entry)
        return ret

pob_conf = PobConfig()
