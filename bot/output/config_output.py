def get_conf_string(name, value):
    conf_item = '{}'.format(name)
    if value and value.lower() != 'true':
        conf_item += ': {}'.format(value.capitalize())
    return conf_item


def get_config_string(config):
    configs = {'Player': [], 'Enemy': [], 'Charges': [], 'Minion':[]}
    for key, entry in config.items():
        abbrev = entry.get('abbreviation')
        value = entry.get('value')
        label = entry.get('label')
        string = get_conf_string(abbrev if abbrev else key, value)
        if label:
            if 'minion' in label.lower():
                configs['Minion'].append(string)

            elif 'you' in label.lower():
                if 'charge' in label.lower():
                    configs['Charges'].append(string)
                else:
                    configs['Player'].append(string)
            elif 'enemy' in label.lower():
                configs['Enemy'].append(string)

                # conf_item = '{}'.format(abbrev if abbrev else key)
                # if value and value.lower() != 'true':
                #     conf_item += ': {}'.format(value.capitalize())
                # strings.append(conf_item)
    out = ''
    for category in configs:
        if len(configs[category])>0:
            print(category)
            out += '**' + category + '**: '
            out += ', '.join(configs[category])
            out += '\n'
    return out if out != '' else None
