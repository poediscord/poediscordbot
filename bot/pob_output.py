from discord import Embed

import config
from bot.output.defense import get_defense
from bot.output.thresholds import OutputThresholds
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


def calc_dps(comparison_dps):
    max = 0
    for dps in comparison_dps:
        if dps and dps > max:
            max = dps
    return round(max, 2)


def get_offense(build):
    # LET THERE BE DIRTY GUIS
    output = ""
    # Basics
    comparison_dps = [build.get_stat('Player', 'TotalDPS'), build.get_stat('Player', 'WithPoisonDPS'),
                      build.get_stat('Minion', 'TotalDPS'), build.get_stat('Minion', 'WithPoisonDPS')]

    dps = calc_dps(comparison_dps)
    output += "**DPS**: {dps:,} @ {speed}/s\n".format(
        dps=dps,
        speed=round(build.stats['Player']['Speed'], 2))

    crit_chance = build.stats['Player']['CritChance']
    crit_multi = build.stats['Player']['CritMultiplier'] * 100
    if crit_chance > OutputThresholds.CRIT_CHANCE.value:
        output += "**Crit**: Chance {crit_chance:,.2f}% | Multiplier: {crit_multi:,.0f}%\n".format(
            crit_chance=crit_chance,
            crit_multi=crit_multi)

    acc = build.stats['Player']['HitChance']
    if acc < OutputThresholds.ACCURACY.value:
        output += "**Hit Chance**: {:.2f}%".format(acc)

    # todo: make a toggle for dot/hits
    return output


def get_config(config):
    strings = []
    for key, val in config.items():
        conf_item = ""
        pob_conf_key = pob_conf.pob_find_entry(key)
        if pob_conf_key and pob_conf_key['abbreviation']:
            abbrev = pob_conf_key['abbreviation']
            conf_item += "{}".format(abbrev if abbrev else key)
            if val.lower() != 'true':
                conf_item += ": {}".format(val.capitalize())
            strings.append(conf_item)
    return ", ".join(strings)


def get_main_skill(build):
    active_skill = build.get_active_skill()
    if active_skill and isinstance(active_skill, Skill):
        output = active_skill.get_links(item=build.get_item(active_skill.slot))
        return output
    else:
        return "None selected"


def generate_minified_output(author, build: Build, inline=True):
    embed = create_embed(author, build.tree, build.level, build.ascendency_name, build.class_name,
                         build.get_active_skill())
    # add new fields
    defense = get_defense(build)
    if defense:
        embed.add_field(name="Defense", value=defense, inline=inline)
    offense = get_offense(build)
    if offense:
        embed.add_field(name="Offense", value=offense, inline=inline)
    # output
    embed.add_field(name='Tree:', value=build.tree)
    return embed


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
