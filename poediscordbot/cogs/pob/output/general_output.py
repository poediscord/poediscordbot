from poediscordbot.cogs.pob.output import attributes_output
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds
from poediscordbot.pob_xml_parser.models.build import Build


def get_resistances(build: Build):
    """
    Creates the resistance string
    :param build: poe_data we want to output
    :return: string containing all resistances or and empty string if nothing is noteworthy
    """
    output = "**Resistances**: "
    resistances = ['Fire', 'Cold', 'Lightning', 'Chaos']
    emojis = [':fire:', ':snowflake:', ':zap:', ':skull:']
    show = False
    for i, res in enumerate(resistances):
        res_val = build.get_player_stat(res + 'Resist', OutputThresholds.CHAOS_RES.value if res == 'Chaos'
        else OutputThresholds.ELE_RES.value)
        res_over_cap = build.get_player_stat(res + 'ResistOverCap')

        if res_val:
            output += emojis[i] + f" {res_val:.0f}"
            show = True
            if res_over_cap and res_over_cap > 0:
                output += f"(+{res_over_cap:.0f}) "
            output += " "
    output += "\n"
    return output if show else ""


def get_basic_line(name, stat, stat_percent, stat_unreserved=0, stat_regen=0, stat_leech_rate=0):
    output = None
    if isinstance(stat, float) and stat > 0 and isinstance(stat_percent, float):
        output = "**" + name + "**: "
        if stat_unreserved and stat - stat_unreserved > 0:
            output += f"{stat_unreserved:,.0f}/"
        output += f"{stat:,.0f}"
        output += f" ({stat_percent:,.0f}%)"
        if stat_regen:
            # Total regen, if displayed is regen - degen.
            output += f" | Reg: {stat_regen:,.0f}/s ({stat_regen / stat * 100:,.1f}%)"
        if stat_leech_rate:
            output += f" | Leech {stat_leech_rate:,.0f}/s ({stat_leech_rate / stat * 100:,.1f}%)"
        output += "\n"
    return output


def get_secondary_def(build: Build):
    """
    Parse all secondary defenses such as armor, eva, dodge, block and display them if they are higher than the thresholds.
    :param build: current poe_data
    :return: String containing noteworthy secondary defense, Empty string as default
    """
    output = ""
    stats = []
    effective_life = max(
        filter(None.__ne__, [build.get_player_stat('Life'), build.get_player_stat('EnergyShield'), 0]))

    armour = build.get_player_stat('Armour', min(OutputThresholds.ARMOUR.value, effective_life))
    stats.append(f"Armour: {armour:,.0f}") if armour and armour else None

    evasion = build.get_player_stat('Evasion', min(OutputThresholds.EVASION.value, effective_life))
    stats.append(f"Evasion: {evasion:,.0f}") if evasion else None

    dodge = build.get_player_stat('AttackDodgeChance', OutputThresholds.DODGE.value)
    stats.append(f"Dodge: {dodge:,.0f}%") if dodge else None

    spell_dodge = build.get_player_stat('SpellDodgeChance', OutputThresholds.SPELL_DODGE.value)
    stats.append(f"Spell Dodge: {spell_dodge:,.0f}%") if spell_dodge else None

    block = build.get_player_stat('BlockChance', OutputThresholds.BLOCK.value)
    stats.append(f"Block: {block:,.0f}%") if block else None

    spell_block = build.get_player_stat('SpellBlockChance', OutputThresholds.SPELL_BLOCK.value)
    stats.append(f"Spell Block: {spell_block:,.0f}%") if spell_block else None

    total_move_speed = build.get_player_stat('EffectiveMovementSpeedMod', 2)
    if total_move_speed:
        movement_speed = (total_move_speed - 1) * 100
        stats.append(
            f"Movement Speed: {movement_speed:.0f}%") if movement_speed > OutputThresholds.MOVE_SPEED.value else None

    if len(stats) > 0:
        output += " | ".join([s for s in stats if s]) + "\n"
    return "**Secondary:** " + output if output != "" else None


def get_keystones(keystones: list, minified=False):
    keystone_strs = [keystone['name'] if not minified else keystone['abbrev'] for keystone in keystones]
    return "**Keystones**: " + ", ".join(keystone_strs)


def get_defense_string(build: Build):
    output = ""
    life_percent_threshold = min(OutputThresholds.LIFE_PERCENT.value,
                                 OutputThresholds.LIFE_PERCENT_PER_LEVEL.value * build.level)
    life_flat = build.get_player_stat('Life')
    life_string = get_basic_line("Life", life_flat,
                                 build.get_player_stat('Spec:LifeInc', life_percent_threshold),
                                 stat_regen=build.get_player_stat('LifeRegen'),
                                 stat_unreserved=build.get_player_stat('LifeUnreserved'),
                                 stat_leech_rate=build.get_player_stat('LifeLeechGainRate',
                                                                       life_flat * OutputThresholds.LEECH.value if life_flat else 0))
    if life_string:
        output += life_string

    es_percent_threshold = min(OutputThresholds.ES_PERCENT.value,
                               OutputThresholds.ES_PERCENT_PER_LEVEL.value * build.level)
    es_flat = build.get_player_stat('EnergyShield')
    es_string = get_basic_line("Energy Shield", es_flat,
                               build.get_player_stat('Spec:EnergyShieldInc', es_percent_threshold),
                               stat_regen=build.get_player_stat('EnergyShieldRegen'),
                               stat_leech_rate=build.get_player_stat('EnergyShieldLeechGainRate',
                                                                     es_flat * OutputThresholds.LEECH.value if es_flat else 0))
    if es_string:
        output += es_string

    net_regen = build.get_player_stat('NetLifeRegen')

    if net_regen:
        output += f"**Net Regen**: {net_regen:,.0f}/s\n"
    mana_flat = build.get_player_stat('Mana')
    mana_string = get_basic_line("Mana", mana_flat, build.get_player_stat('Spec:ManaInc'),
                                 stat_regen=build.get_player_stat('ManaRegen'),
                                 stat_unreserved=build.get_player_stat('ManaUnreserved'),
                                 stat_leech_rate=build.get_player_stat('ManaLeechGainRate',
                                                                       mana_flat * OutputThresholds.LEECH.value if mana_flat else 0))
    if mana_string:
        output += mana_string

    # todo: only pass necessary values to the following options:
    secondary_def = get_secondary_def(build)
    if secondary_def:
        output += secondary_def
    output += get_resistances(build)

    attributes = attributes_output.get_attributes(build.get_player_stat('Str'), build.get_player_stat('Int'),
                                                  build.get_player_stat('Dex'))
    if attributes:
        output += attributes

    if build.keystones:
        output += get_keystones(build.keystones)
    return output
