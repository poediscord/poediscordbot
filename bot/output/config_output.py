def prepare_config_line(name, value):
    """
    Create the entry for one specific configuration with it's name and value
    :param name:
    :param value:
    :return: string
    """
    conf_item = '{}'.format(name)
    if value and value.lower() != 'true':
        conf_item += ': {}'.format(value.capitalize())
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
        string = prepare_config_line(abbrev if abbrev else key, value)
        if category:
            configs.setdefault(category.capitalize(),[]).append(string)

    out = ''
    for category in configs:
        if len(configs[category])>0:
            out += '**' + category + '**: '
            out += ', '.join(configs[category])
            out += '\n'
    return out if out != '' else None
