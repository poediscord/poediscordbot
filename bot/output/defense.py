from bot.output.thresholds import OutputThresholds
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


def get_basic_line(name, basic_stat, basic_stat_percent, stat_unreserved=0, basic_stat_regen=0):
    output = None
    print(name, basic_stat, basic_stat_percent, basic_stat_regen)
    if isinstance(basic_stat, float) and isinstance(basic_stat_percent, float):
        print("GO")
        output = "**" + name + "**: "
        if stat_unreserved and basic_stat - stat_unreserved > 0:
            output += "{unreserved:.0f}/".format(unreserved=stat_unreserved)
        output += "{stat:.0f}".format(stat=basic_stat)
        output += " ({stat_percent:.0f}%)".format(stat_percent=basic_stat_percent)
        if basic_stat_regen:
            # Total regen, if displayed is regen - degen.
            output += " | Regen: {regen:.0f}/s".format(regen=basic_stat_regen)
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
    armour = build.get_stat('Player', 'Armour')
    stats.append("Armour: {:.0f}".format(armour)) if armour and armour > OutputThresholds.ARMOUR.value else None

    evasion = build.get_stat('Player', 'Evasion', OutputThresholds.EVASION.value)
    stats.append("Evasion: {:.0f}".format(evasion)) if evasion else None

    dodge = build.get_stat('Player', 'AttackDodgeChance', OutputThresholds.DODGE.value)
    stats.append("Dodge: {:.0f}%".format(dodge)) if dodge else None

    spell_dodge = build.get_stat('Player', 'SpellDodgeChance', OutputThresholds.SPELL_DODGE.value)
    stats.append("Spell Dodge: {:.0f}%".format(spell_dodge)) if spell_dodge else None

    block = build.get_stat('Player', 'BlockChance', OutputThresholds.BLOCK.value)
    stats.append("Block: {:.0f}%".format(block)) if block else None

    spell_block = build.get_stat('Player', 'SpellBlockChance', OutputThresholds.SPELL_BLOCK.value)
    stats.append("Spell Block: {:.0f}%".format(spell_block)) if spell_block  else None
    if len(stats) > 0:
        output += " | ".join([s for s in stats if s]) + "\n"
    return "**Secondary:** " + output if output != "" else None


def get_defense(build: Build):
    output = ""
    life_percent_threshold = min(OutputThresholds.LIFE_PERCENT.value,
                                 OutputThresholds.LIFE_PERCENT_PER_LEVEL.value * build.level)
    life_string = get_basic_line("Life", build.get_stat('Player', 'Life'),
                                 build.get_stat('Player', 'Spec:LifeInc', life_percent_threshold),
                                 basic_stat_regen=build.get_stat('Player', 'LifeRegen'),
                                 stat_unreserved=build.get_stat('Player', 'LifeUnreserved'))
    if life_string:
        output += life_string

    es_percent_threshold = min(OutputThresholds.ES_PERCENT.value,
                               OutputThresholds.ES_PERCENT_PER_LEVEL.value * build.level)
    es_string = get_basic_line("Energy Shield", build.get_stat('Player', 'EnergyShield'),
                               build.get_stat('Player', 'Spec:EnergyShieldInc', es_percent_threshold),
                               basic_stat_regen=build.get_stat('Player', 'EnergyShieldRegen'))
    if es_string:
        output += es_string

    net_regen = build.get_stat('Player', 'NetLifeRegen')

    if net_regen:
        output += "**Net Regen**: {:.0f}/s\n".format(net_regen)

    mana_string = get_basic_line("Mana", build.get_stat('Player', 'Mana'), build.get_stat('Player', 'Spec:ManaInc'),
                                 basic_stat_regen=build.get_stat('Player', 'ManaRegen'),
                                 stat_unreserved=build.get_stat('Player', 'ManaUnreserved'))
    print(mana_string)
    if mana_string:
        output += mana_string

    # todo: only pass necessary values to the following options:
    secondary_def = get_secondary_def(build)
    if secondary_def:
        output += secondary_def
    output += get_resistances(build)

    return output
