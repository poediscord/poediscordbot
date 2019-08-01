from poediscordbot.pob_xml_parser.models import Build


def get_charges(build: Build, charge_types=['Endurance', 'Frenzy', 'Power']):
    output = []

    for charge_type in charge_types:
        val = build.get_stat('Player', charge_type + 'Charges')
        max_val = build.get_stat('Player',
                                 charge_type + 'ChargesMax')

        charge_is_active = build.config.get('use' + charge_type + "Charges")
        if charge_is_active and val and max_val:
            output.append(f'{charge_type}: {val:.0f}/{max_val:.0f}')

    return ', '.join(output) if len(output) > 0 else None
