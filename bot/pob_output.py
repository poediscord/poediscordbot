from discord import Embed

import config
from models import Build, Gem, Skill
from util.translate_pob_conf import pob_conf


def wrap_codeblock(string, lang='css'):
    return '```' + lang + '\n' + string + '```'


def create_embed(author, tree, level, ascendency_name, class_name, main_skill: Skill):
    embed = Embed(title='tmp', color=config.color)
    gem_name = "Undefined"
    if main_skill:
        main_gem = main_skill.get_selected()
        if isinstance(main_gem, Gem):
            gem_name = main_gem.name

    if ascendency_name or class_name:
        url = 'https://raw.githubusercontent.com/FWidm/discord-pob/master/_img/' + (
            ascendency_name if ascendency_name != "None" else class_name) + '.png'
        embed.set_thumbnail(url=url)
        # url='http://web.poecdn.com/image/Art/2DArt/SkillIcons/passives/Ascendants/' + ascendency_name + '.png')

    embed.title = "{gem} - {char} (Lvl: {level})".format(
        char=class_name if ascendency_name.lower() == 'none' else ascendency_name,
        gem=gem_name,
        level=level)
    if author:
        embed.title += " by " + author.name
    return embed


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
        crit_ch=build.stats['CritChance'],
        crit_dam=build.stats['CritMultiplier'] * 100)
    output += "**Hit Chance**: {:.2f}%".format(build.stats['HitChance'])
    # todo: make a toggle for dot/hits
    return output


def get_config(config):
    output = ""
    if len(config) < 1:
        return
    for key, val in config.items():
        key = pob_conf.pob_find_entry(key)['label']
        output += "{} - {};\t".format(key, val.capitalize())
    return output


def get_main_skill(build):
    active_skill = build.get_active_skill()
    if active_skill and isinstance(active_skill, Skill):
        output = active_skill.get_links(item=build.get_item(active_skill.slot))
        return output
    else:
        return "None selected"


def generate_output(author, build: Build, inline=False):
    embed = create_embed(author, build.tree, build.level, build.ascendency_name, build.class_name,
                         build.get_active_skill())
    # print(build.stats)
    # print(build.config)

    # add new fields
    defense = get_defense(build)
    if defense:
        embed.add_field(name="Defense", value=defense, inline=inline)
    offense = get_offense(build)
    if offense:
        embed.add_field(name="Offense", value=offense, inline=inline)
    skill = get_main_skill(build)
    if skill:
        embed.add_field(name="Main Skill", value=skill, inline=inline)
    config = get_config(build.config)
    if config:
        embed.add_field(name="Config", value=config, inline=inline)

    # output
    embed.add_field(name='Tree:', value=build.tree)
    return embed
