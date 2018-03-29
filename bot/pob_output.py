from discord import Embed

import config
from bot.output import defense_output, config_output, charges_output, skill_output, offense_output
from models import Build, Gem, Skill


def wrap_codeblock(string, lang='css'):
    return '```' + lang + '\n' + string + '```'


def create_embed(author, level, ascendency_name, class_name, main_skill: Skill):
    """
    Create the basic embed we add information to
    :param author: of the parsed message - str
    :param tree: enclosed tree information
    :param level: of the build
    :param ascendency_name: to display
    :param class_name: to display if no ascendency has been chosen
    :param main_skill: main skill to display
    :return (Embed): the created Embed with the options set.
    """
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
        embed.title += " by: " + author.name
    return embed


def generate_response(author, build: Build, minified=False):
    """
    Build an embed to respond to the user.
    :param author: name of the person triggering the action
    :param build: build to parse an embed from
    :param minified (bool): whether to get a minified version or the full one
    :return: Filled embed for discord
    """
    embed = create_embed(author, build.level, build.ascendency_name, build.class_name,
                         build.get_active_skill())
    # add new fields
    def_str = defense_output.get_defense_string(build)
    if def_str:
        embed.add_field(name="Defense", value=def_str, inline=minified)
    offense = offense_output.get_offense(build)
    if offense:
        embed.add_field(name="Offense", value=offense, inline=minified)
    charges_str = charges_output.get_charges(build)
    if charges_str:
        embed.add_field(name="Charges", value=charges_str, inline=minified)
    # if not minified, add detailed infos.
    if not minified:
        skill = skill_output.get_main_skill(build)
        if skill:
            embed.add_field(name="Main Skill", value=skill, inline=minified)
        conf_str = config_output.get_config_string(build.config)
        if conf_str:
            embed.add_field(name="Config", value=conf_str, inline=minified)
    # output
    embed.add_field(name='Tree:', value=build.tree)
    return embed
