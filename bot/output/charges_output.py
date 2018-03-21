from bot.output.thresholds import OutputThresholds
from models import Build


def get_charges(build: Build, charge_types=['Endurance', 'Frenzy', 'Power']):
    output = []

    for charge_type in charge_types:
        val = build.get_stat('Player', charge_type + 'Charges')
        max_val = build.get_stat('Player',
                                 charge_type + 'ChargesMax')

        charge_is_active = build.config.get('use' + charge_type + "Charges")
        print(charge_type, val, max_val, charge_is_active)
        if charge_is_active and val and max_val:
            output.append('{}: {:.0f}/{:.0f}'.format(charge_type, val, max_val))

    return ', '.join(output) if len(output) > 0 else None
