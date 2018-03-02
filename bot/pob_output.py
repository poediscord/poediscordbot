from discord import Embed

import config
from models import Build, Gem


def wrap_codeblock(string, lang='css'):
    return '```' + lang + '\n' + string + '```'


def create_embed(author, tree, level, ascendency_name, class_name, main_skill: Gem):
    embed = Embed(title='tmp', color=config.color)

    if ascendency_name and ascendency_name != "":
        embed.set_thumbnail(
            url='http://web.poecdn.com/image/Art/2DArt/SkillIcons/passives/Ascendants/' + ascendency_name + '.png')

    embed.title = "{gem} - {char} (Lvl: {level})".format(
        char=class_name if ascendency_name.lower() == 'none' else ascendency_name,
        gem=main_skill.name if main_skill.name else 'Undefined',
        level=level)
    if author:
        embed.title += " by " + author.name
    return embed


def add_line(param):
    print(param)
    line = ""
    for key in param:
        print(key, param[key])
        line += '**{key}**: {val}'
    line += "\n"
    # "**Energy Shield**: {es} ({es_inc}%); **Regen**: {es_regen}\n".format(es=build.stats['EnergyShield'],
    #                                                                                 es_inc=build.stats[
    #                                                                                     'Spec:EnergyShieldInc'],
    #                                                                                 es_regen=build.stats[
    #                                                                                     'EnergyShieldRegen'])


def get_defense(build: Build):
    # LET THERE BE DIRTY GUIS
    output = ""
    # Basics
    output += "**Life**: {life:.0f} ({life_inc:.0f}%) | **Regen**: {life_regen:.1f}/s\n".format(
        life=build.stats['Life'],
        life_inc=build.stats[
            'Spec:LifeInc'],
        life_regen=build.stats['LifeRegen'])

    output += "**Energy Shield**: {es:.0f} ({es_inc:.0f}%) | **Regen**: {es_regen:.1f}/s\n".format(
        es=build.stats['EnergyShield'],
        es_inc=build.stats[
            'Spec:EnergyShieldInc'],
        es_regen=build.stats[
            'EnergyShieldRegen'])

    output += "**Mana**: {mana:.0f} ({mana_inc:.0f}%)| **Regen**: {mana_regen:.1f}/s\n".format(mana=build.stats['Mana'],
                                                                                               mana_inc=build.stats[
                                                                                                   'Spec:ManaInc'],
                                                                                               mana_regen=build.stats[
                                                                                                   'ManaRegen'])
    # Res
    output += ":fire: {:.0f}".format(build.stats['FireResist'])
    if int(build.stats['FireResistOverCap']) > 0:
        output += "(+{:.0f}) ".format(build.stats['FireResistOverCap'])
    output += " | "

    output += ":snowflake: {:.0f}".format(build.stats['ColdResist'])
    if int(build.stats['ColdResistOverCap']) > 0:
        output += "(+{:.0f}) ".format(build.stats['ColdResistOverCap'])
    output += " | "

    output += ":zap: {:.0f}".format(build.stats['LightningResist'])
    if int(build.stats['ColdResistOverCap']) > 0:
        output += "(+{:.0f}) ".format(build.stats['LightningResistOverCap'])
    output += " | "

    output += ":skull: {:.0f}".format(build.stats['ChaosResist'])
    if int(build.stats['ChaosResistOverCap']) > 0:
        output += "(+{:.0f}) ".format(build.stats['ChaosResistOverCap'])
    output += "\n"
    # add_line({'es': build.stats['EnergyShield'], 'life': build.stats['Life']})
    return output


def get_offense(build):
    # LET THERE BE DIRTY GUIS
    output = ""
    # Basics
    output += "**DPS**: {dps:,} @ {speed}/s\n".format(
        dps=round(max([build.stats['TotalDPS'], build.stats['WithPoisonDPS']]), 2),
        speed=round(build.stats['Speed'], 2))
    output += "**Crit**: Chance {crit_ch:,.2f}% | Damage: {crit_dam:,.0f}%\n".format(
        crit_ch=build.stats['CritChance'] * 10,
        crit_dam=build.stats['CritMultiplier'] * 100)
    output += "**Hit Chance**: {:.2f}%".format(build.stats['HitChance'])
    # todo: make a toggle for dot/hits
    return output


def get_config(config):
    output = ""
    for key, val in config.items():
        if val == 'true':
            output += "{}\t".format(key)
        else:
            output += "{}: {}\t".format(key, val)

    output += "\n"
    return output


def generate_output(author, build: Build):
    embed = create_embed(author, build.tree, build.level, build.ascendency_name, build.class_name,
                         build.get_active_skill())
    print(build.stats)
    print(build.config)

    # add new fields
    embed.add_field(name="Defense", value=get_defense(build), inline=False)
    embed.add_field(name="Offense", value=get_offense(build), inline=False)
    embed.add_field(name="Config", value=get_config(build.config), inline=False)

    # output
    embed.add_field(name='Tree:', value=build.tree)
    return embed
