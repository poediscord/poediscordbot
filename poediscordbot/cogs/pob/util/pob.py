import json
import re
from datetime import datetime, timedelta
from urllib import request

from instance import config

from poediscordbot.pob_xml_parser.models.skill import Skill
from poediscordbot.util.logging import log

POB_CONF_JSON = 'resources/pob_conf.json'
POB_SPECTRES = 'resources/pob_spectres.json'


class PobConfig:
    COMMUNITY_POB_RAW_GITHUB_URL = "https://raw.githubusercontent.com/PathOfBuildingCommunity/PathOfBuilding/master/"

    def __init__(self, path_to_pob_conf=POB_CONF_JSON):
        self.config = self.get_config(path_to_pob_conf)

    def fetch_config_entry(self, config_var: str):
        """
        Reads the pob_config.json and finds the specific entries that are needed.
        :param config_var: config variable
        :return: entry
        """
        for entry in self.config['conf']:
            if entry == config_var:
                return self.config['conf'].get(entry)

    def get_config(self, path_to_pob_conf):
        loaded_conf = None
        file_path = config.ROOT_DIR + path_to_pob_conf
        try:
            loaded_conf = json.load(open(file_path))
        except FileNotFoundError as err:
            log.error(f'{path_to_pob_conf} is missing, trying to obtain a new copy... err was "{err}"')

        if loaded_conf:
            week_ago_date = datetime.now() - timedelta(days=7)
            # json_date = datetime.fromisoformat(loaded_conf['utc-date']) todo: enable when pypy 3.7 exists
            json_date = datetime.strptime(loaded_conf['utc-date'], "%Y-%m-%dT%H:%M:%S.%f")
            # if json date is older than a week, update
            if json_date < week_ago_date:
                self.fetch_config(file_path)
                log.info(f"finished creating new {path_to_pob_conf}.json in resources...")
                loaded_conf = json.load(open(file_path))

        if not loaded_conf:
            self.fetch_config(path_to_pob_conf)
            log.info(f"finished creating new {path_to_pob_conf}.json in resources...")
            loaded_conf = json.load(open(file_path))

        return loaded_conf

    @staticmethod
    def fetch_config(path_to_pob_conf):
        """
        Read the current PoB master branch configoptions and create a json file for it.
        """
        url = f"{PobConfig.COMMUNITY_POB_RAW_GITHUB_URL}src/Modules/ConfigOptions.lua"
        url = request.urlopen(url)
        content = url.read().decode('utf-8')
        conditions = [line.strip() for line in content.split('{ var') if
                      "condition" in line.lower() or "ifflag" in line.lower()]
        keywords = ['var', 'label', 'ifOption', 'ifSkill', 'ifSkillList']
        regex = r'(\w+)\s*=\s*((?:"[^"]+")|{(?:\s*"[^"]+",?\s*)+})'

        attributes = {}
        for condition in conditions:
            attribute = {}
            condition = "var " + re.sub(r'{ label(.|\s)+$', '', condition)
            matches = re.findall(regex, condition)

            for m in matches:
                key = m[0].strip()
                val = m[1].strip()

                if val.startswith('"'):
                    val = val.replace('"', '')
                elif val.startswith('{'):
                    val = list(
                        map(lambda v: v.replace('"', '').replace('{', '').replace('}', '').strip(), val.split(',')))

                if key not in attribute and key in keywords:
                    attribute[key] = val

            if any(key in keywords for key in attribute):
                attributes[attribute['var']] = attribute

        pob_config_content = {'utc-date': datetime.utcnow().isoformat(), 'conf': attributes}
        try:
            with open(path_to_pob_conf, 'r') as file:
                file_content = json.load(file)
                if 'conf' in file_content:
                    # we need to do this to keep manually entered values in our file such as category
                    for confkey in file_content['conf']:
                        print(f">> {file_content['conf'][confkey]}")
                        if confkey in attributes:
                            file_content['conf'][confkey].update(attributes[confkey])
                        else:
                            log.error(f"Skipped config key: Please inform the bot author that the key '{confkey}' "
                                      f"could not be parsed.")

                    new_keys = [key for key in attributes if not any(k == key for k in file_content['conf'])]
                    print(new_keys)
                    for key in new_keys:
                        file_content['conf'][key] = attributes[key]

                    pob_config_content = {'utc-date': datetime.utcnow().isoformat(), 'conf': file_content['conf']}
        except FileNotFoundError:
            pass

        with open(path_to_pob_conf, 'w') as file:
            json.dump(pob_config_content, file, indent=4)


class PobMinionLookup(object):
    def __init__(self, path_to_spectres=POB_SPECTRES):
        file_path = config.ROOT_DIR + path_to_spectres
        try:
            self.spectres = json.load(open(file_path))
        except FileNotFoundError as err:
            log.error(f'{path_to_spectres} is missing, trying to obtain a new copy... err was "{err}"')
            self.fetch_spectres(file_path)
            log.info(f"finished creating new {path_to_spectres} in resources...")
            self.spectres = json.load(open(file_path))

    def get_monster_name(self, minion_info, main_skill: Skill):
        # do in memory translation of any normal mobs we need to mention in addition to the skill for now only phantasms
        if minion_info and '\\' not in minion_info:
            if 'SummonedPhantasm' in minion_info \
                    and any([gem for gem in main_skill.gems if 'SupportSummonGhostOnKill' in gem.id]):
                return 'Summoned Phantasm'
            if 'AxisEliteSoldierHeraldOfLight' in minion_info:
                return 'Sentinel of Purity'
        # if we have any backslash in the name we have to look up spectre paths and translate them to names
        return self.spectres['spectres'].get(minion_info)

    @staticmethod
    def fetch_spectres(file_path):
        """
        Read the current PoB master branch 3_0 spectre file  and create a json file for it.
        """
        url = f"{PobConfig.COMMUNITY_POB_RAW_GITHUB_URL}src/Data/Spectres.lua"
        url = request.urlopen(url)
        content = url.read().decode('utf-8')

        regex = r'minions\[\"(?P<path>.*)\"\].*\s*name = \"(?P<name>.*)\"'
        matches = re.findall(regex, content, re.MULTILINE)
        spectre_dict = {m[0]: m[1] for m in matches}

        file_content = {'utc-date': datetime.utcnow().isoformat(), 'spectres': spectre_dict}

        with open(file_path, 'w') as file:
            json.dump(file_content, file, indent=4)


pob_conf = PobConfig()

pob_minions = PobMinionLookup()
