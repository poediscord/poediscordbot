from poediscordbot.util.logging import log


def special_ignored_case(name, value):
    if name == 'Exposure to' and value == '0':
        return True
    return False


def prepare_config_line(name, value):
    """
    Create the entry for one specific configuration with it's name and value
    :param name:
    :param value:
    :return: string
    """
    conf_item = f'{name}'
    if not special_ignored_case(name, value):
        if value and value.lower() != 'true':
            conf_item += f': {value.capitalize()}'
        return conf_item


def get_config_string(config):
    """
    Use the given config to extract one string for the output.
    :param config: a dictionary of configs from a Build object
    :return: string representation
    """
    configs = {}
    for key, entry in config.items():
        abbrev = entry.get('abbreviation')
        value = entry.get('value')
        category = entry.get('category')
        config_line = prepare_config_line(abbrev if abbrev else key, value)
        if category and config_line:
            configs.setdefault(category.capitalize(), []).append(config_line)
        else:
            log.warn(f"Category='{category}' or config_line='{config_line}' not set or unknown, check 'pob_conf.json'"
                     f"for entries with mixing categories and abbreviations. "
                     f"This happens after pob introduces new values. If one of the values is None you need to "
                     f"update the json file similarly to the existing entries.")
    out = ''
    for category in configs:
        if len(configs[category]) > 0:
            out += '**' + category + '**: '
            out += ', '.join(configs[category])
            out += '\n'
    return out if out != '' else None
