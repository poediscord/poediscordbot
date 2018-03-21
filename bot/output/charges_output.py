from bot.output.thresholds import OutputThresholds
from models import Build


def get_charges(build: Build):
    output = []

    charge_types = ['Endurance', 'Frenzy', 'Power']
    for charge_type in charge_types:
        val, max_val = build.get_stat('Player', charge_type + 'Charges'), build.get_stat('Player',
                                                                                         charge_type + 'ChargesMax')
        if max_val >= OutputThresholds.CHARGE_MAXIMUM.value:
            output.append('{}: {:.0f}/{:.0f}'.format(charge_type, val, max_val))

    return ', '.join(output) if len(output)>0 else None
