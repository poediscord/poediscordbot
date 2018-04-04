from bot.consts.thresholds import OutputThresholds
from models import Build


def get_resistances(build: Build, force_display=False):
    """
    Creates the resistance string
    :param build: build we want to output
    :param normal_res_cap: values above this threshold are displayed
    :param force_display:  override threshold
    :return: string containing all resistances or and empty string if nothing is noteworthy
    """
    output = "**Resistances**: "
    resistances = ['Fire', 'Cold', 'Lightning', 'Chaos']
    emojis = [':fire:', ':snowflake:', ':zap:', ':skull:']
    show = False
    for i, res in enumerate(resistances):
        res_val = build.get_stat('Player', res + 'Resist', OutputThresholds.CHAOS_RES.value if res == 'Chaos'
        else OutputThresholds.ELE_RES.value)
        res_over_cap = build.get_stat('Player', res + 'ResistOverCap')

        if res_val:
            output += emojis[i] + " {:.0f}".format(res_val)
            show = True
            if res_over_cap and res_over_cap > 0:
                output += "(+{:.0f}) ".format(res_over_cap)
            output += " "
    output += "\n"
    return output if show else ""


def get_basic_line(name, stat, stat_percent, stat_unreserved=0, stat_regen=0, stat_leech_rate=0):
    output = None
    if isinstance(stat, float) and stat > 0 and isinstance(stat_percent, float):
        output = "**" + name + "**: "
        if stat_unreserved and stat - stat_unreserved > 0:
            output += "{unreserved:,.0f}/".format(unreserved=stat_unreserved)
        output += "{stat:,.0f}".format(stat=stat)
        output += " ({stat_percent:,.0f}%)".format(stat_percent=stat_percent)
        if stat_regen:
            # Total regen, if displayed is regen - degen.
            output += " | Regen: {regen:,.0f}/s".format(regen=stat_regen)
        if stat_leech_rate:
            output += " | Leech {leech:,.0f}/s".format(leech=stat_leech_rate)
        output += "\n"
    return output


def get_secondary_def(build: Build):
    """
    Parse all secondary defenses such as armor, eva, dodge, block and display them if they are higher than the thresholds.
    :param build: current build
    :return: String containing noteworthy secondary defense, Empty string as default
    """
    output = ""
    stats = []
    effective_life = max(
        filter(None.__ne__, [build.get_stat('Player', 'Life'), build.get_stat('Player', 'EnergyShield')]))

    armour = build.get_stat('Player', 'Armour', min(OutputThresholds.ARMOUR.value, effective_life))
    stats.append("Armour: {:,.0f}".format(armour)) if armour and armour else None

    evasion = build.get_stat('Player', 'Evasion', min(OutputThresholds.EVASION.value, effective_life))
    stats.append("Evasion: {:,.0f}".format(evasion)) if evasion else None

    dodge = build.get_stat('Player', 'AttackDodgeChance', OutputThresholds.DODGE.value)
    stats.append("Dodge: {:,.0f}%".format(dodge)) if dodge else None

    spell_dodge = build.get_stat('Player', 'SpellDodgeChance', OutputThresholds.SPELL_DODGE.value)
    stats.append("Spell Dodge: {:,.0f}%".format(spell_dodge)) if spell_dodge else None

    block = build.get_stat('Player', 'BlockChance', OutputThresholds.BLOCK.value)
    stats.append("Block: {:,.0f}%".format(block)) if block else None

    spell_block = build.get_stat('Player', 'SpellBlockChance', OutputThresholds.SPELL_BLOCK.value)
    stats.append("Spell Block: {:,.0f}%".format(spell_block)) if spell_block  else None
    if len(stats) > 0:
        output += " | ".join([s for s in stats if s]) + "\n"
    return "**Secondary:** " + output if output != "" else None


def get_defense_string(build: Build):
    output = ""
    life_percent_threshold = min(OutputThresholds.LIFE_PERCENT.value,
                                 OutputThresholds.LIFE_PERCENT_PER_LEVEL.value * build.level)
    life_flat = build.get_stat('Player', 'Life')
    life_string = get_basic_line("Life", life_flat,
                                 build.get_stat('Player', 'Spec:LifeInc', life_percent_threshold),
                                 stat_regen=build.get_stat('Player', 'LifeRegen'),
                                 stat_unreserved=build.get_stat('Player', 'LifeUnreserved'),
                                 stat_leech_rate=build.get_stat('Player', 'LifeLeechGainRate',
                                                                life_flat * OutputThresholds.LEECH.value))
    if life_string:
        output += life_string

    es_percent_threshold = min(OutputThresholds.ES_PERCENT.value,
                               OutputThresholds.ES_PERCENT_PER_LEVEL.value * build.level)
    es_flat = build.get_stat('Player', 'EnergyShield')
    es_string = get_basic_line("Energy Shield", es_flat,
                               build.get_stat('Player', 'Spec:EnergyShieldInc', es_percent_threshold),
                               stat_regen=build.get_stat('Player', 'EnergyShieldRegen'),
                               stat_leech_rate=build.get_stat('Player', 'EnergyShieldLeechGainRate',
                                                              es_flat * OutputThresholds.LEECH.value))
    if es_string:
        output += es_string

    net_regen = build.get_stat('Player', 'NetLifeRegen')

    if net_regen:
        output += "**Net Regen**: {:,.0f}/s\n".format(net_regen)
    mana_flat = build.get_stat('Player', 'Mana')
    mana_string = get_basic_line("Mana", mana_flat, build.get_stat('Player', 'Spec:ManaInc'),
                                 stat_regen=build.get_stat('Player', 'ManaRegen'),
                                 stat_unreserved=build.get_stat('Player', 'ManaUnreserved'),
                                 stat_leech_rate=build.get_stat('Player', 'ManaLeechGainRate',
                                                                mana_flat * OutputThresholds.LEECH.value))
    if mana_string:
        output += mana_string

    # todo: only pass necessary values to the following options:
    secondary_def = get_secondary_def(build)
    if secondary_def:
        output += secondary_def
    output += get_resistances(build)

    return output
