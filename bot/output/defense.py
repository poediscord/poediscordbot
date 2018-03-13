from models import Build


def get_resistances(build: Build, normal_res_cap: int, force_display=False):
    """
    Creates the resistance string
    :param build: build we want to output
    :param normal_res_cap: values above this threshold are displayed
    :param force_display:  override threshold
    :return: string containing all resistances
    """
    output = "**Resistances**: "
    resistances = ['Fire', 'Cold', 'Lightning', 'Chaos']
    emojis = [':fire:', ':snowflake:', ':zap:', ':skull:']
    for i, res in enumerate(resistances):
        res_val, res_over_cap = build.stats['Player'][res + 'Resist'], build.stats['Player'][res + 'ResistOverCap']
        if force_display or res_val > normal_res_cap:
            output += emojis[i] + " {:.0f}".format(res_val)
            if res_over_cap > 0:
                output += "(+{:.0f}) ".format(res_over_cap)
            output += " "
    output += "\n"
    return output


def get_basic_line(name, basic_stat, basic_stat_percent, basic_stat_regen, stat_threshold=0, inc_threshold=0,
                   regen_threshold=0):
    output = None
    if basic_stat > stat_threshold:
        output = "**" + name + "**:"
        output += "{stat:.0f} ({stat_percent:.0f}%)".format(
            stat=basic_stat,
            stat_percent=basic_stat_percent)
        if basic_stat_regen > regen_threshold:
            output += " Regen: {regen}".format(regen=basic_stat_regen)
        output += "\n"
    return output


def get_defense(build: Build):
    output = ""
    # Basics
    # output += "**Life**: {life:.0f} ({life_inc:.0f}%) | **Regen**: {life_regen:.1f}/s\n".format(
    #     life=build.stats['Player']['Life'],
    #     life_inc=build.stats['Player'][
    #         'Spec:LifeInc'],
    #     life_regen=build.stats['Player']['LifeRegen'])
    life_str = get_basic_line("Life", build.stats['Player']['Life'], build.stats['Player']['Spec:LifeInc'],
                              build.stats['Player']['LifeRegen'])
    if life_str:
        output += life_str
    output += "**Energy Shield**: {es:.0f} ({es_inc:.0f}%) | **Regen**: {es_regen:.1f}/s\n".format(
        es=build.stats['Player']['EnergyShield'],
        es_inc=build.stats['Player'][
            'Spec:EnergyShieldInc'],
        es_regen=build.stats['Player'][
            'EnergyShieldRegen'])

    output += "**Mana**: {mana:.0f} ({mana_inc:.0f}%)| **Regen**: {mana_regen:.1f}/s\n".format(
        mana=build.stats['Player']['Mana'],
        mana_inc=build.stats['Player'][
            'Spec:ManaInc'],
        mana_regen=build.stats['Player'][
            'ManaRegen'])
    # Res
    normal_res_cap = 75
    output += get_resistances(build, normal_res_cap)
    return output
