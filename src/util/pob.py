import json
from datetime import datetime
from urllib import request

import config
from src import util
from src.util.logging import log


class PobConfig():
    def __init__(self, path_to_pob_conf="pob_conf.json"):
        try:
            self.config = json.load(open(config.ROOT_DIR + '/' + path_to_pob_conf))
        except FileNotFoundError as err:
            log.error("pob_conf is missing, trying to obtain a new copy... err={}".format(err))
            self.fetch_config()

    def fetch_entry(self, config_var: str):
        """
        Reads the pob_config.json and finds the specific entries that are needed.
        :param config_var: config variable
        :return: entry
        """
        for entry in self.config['conf']:
            if entry == config_var:
                return self.config['conf'].get(entry)

    @staticmethod
    def fetch_config():
        """
        Read the current PoB master branch configoptions and create a json file for it.
        """
        url = "https://raw.githubusercontent.com/Openarl/PathOfBuilding/master/Modules/ConfigOptions.lua"
        url = request.urlopen(url)
        content = url.read().decode('utf-8')
        conditions = [line.strip() for line in content.split('{ var') if
                      "condition" in line.lower() or "ifflag" in line.lower()]
        keywords = ['var', 'label']

        attributes = {}
        for condition in conditions:
            attribute = {}
            for attr in ('var ' + condition).split(', '):
                if any(util.starts_with(keyword, attr) and '}' not in attr for keyword in keywords) and ' = ' in attr:
                    key, val = attr.split(' = ')
                    val = val.replace('"', '')
                    attribute[key] = val
            if all(key in keywords for key in attribute):
                attributes[attribute['var']] = attribute

        pob_config_content = {'utc-date': datetime.utcnow().isoformat(), 'conf': attributes}
        try:
            with open('pob_conf.json', 'r') as file:
                file_content = json.load(file)
                if 'conf' in file_content:
                    # we need to do this to keep manually entered values in our file such as category
                    for confkey in file_content['conf']:
                        print(">> {}".format(file_content['conf'][confkey]))
                        file_content['conf'][confkey].update(attributes[confkey])

                    new_keys = [key for key in attributes if not any(k == key for k in file_content['conf'])]
                    print(new_keys)
                    for key in new_keys:
                        file_content['conf'][key] = attributes[key]

                    pob_config_content = {'utc-date': datetime.utcnow().isoformat(), 'conf': file_content['conf']}
        except FileNotFoundError:
            pass

        with open('pob_conf.json', 'w') as file:
            json.dump(pob_config_content, file, indent=4)


pob_conf = PobConfig()
