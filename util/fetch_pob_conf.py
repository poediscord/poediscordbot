import urllib.request

import re
import json

from datetime import datetime, timezone
from pprint import pprint

import util

"""
Read the current PoB master branch configoptions and create a json file for it.
"""
url = "https://raw.githubusercontent.com/Openarl/PathOfBuilding/master/Modules/ConfigOptions.lua"
url = urllib.request.urlopen(url)
content = url.read().decode('utf-8')
conditions = [line.strip() for line in content.split('{ var') if "condition" in line.lower()]
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

# pprint(attributes)
# todo: instead of replacing the file we could just add new fields

with open('pob_conf.json', 'r') as file:
    file_content = json.load(file)
    if 'conf' in file_content:
        for confkey in file_content['conf']:
            print(">> {}".format(file_content['conf'][confkey]))
            file_content['conf'][confkey].update(attributes[confkey])
            print("<< {}".format(file_content['conf'][confkey]))
        pob_config_content = {'utc-date': datetime.utcnow().isoformat(), 'conf': file_content['conf']}
        with open('pob_conf.json', 'w') as file:
            json.dump(pob_config_content, file, indent=4)
