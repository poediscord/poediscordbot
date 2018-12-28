from discord import Embed

import config
from src.bot.output import config_output, charges_output, skill_output, offense_output, general_output
from src.bot.util import build_checker
from src.models import Build, Gem, Skill
from util.tree import poe_tree_codec


def create_embed(author, level, ascendency_name, class_name, main_skill: Skill, is_support):
    """
    Create the basic embed we add information to
    :param author: of the parsed message - str
    :param level: of the build
    :param ascendency_name: to display
    :param class_name: to display if no ascendency has been chosen
    :param main_skill: main skill to display
    :return (Embed): the created Embed with the options set.
    """
    embed = Embed(title='tmp', color=config.color)
    gem_name = "Undefined"
    if is_support:
        gem_name = "Support"
    elif main_skill:
        main_gem = main_skill.get_selected()
        if isinstance(main_gem, Gem):
            gem_name = main_gem.get_name()

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
        displayed_name = None
        try:
            displayed_name = author.nick
        except AttributeError:
            pass
        if not displayed_name:
            displayed_name = author.name

        if displayed_name:
            embed.title += " by: " + displayed_name
    return embed


def generate_response(author, build: Build, minified=False, pastebin=None, consts=None):
    """
    Build an embed to respond to the user.
    :param consts: poe constants - skill info
    :param author: name of the person triggering the action
    :param build: build to parse an embed from
    :param minified (bool): whether to get a minified version or the full one
    :return: Filled embed for discord
    """
    is_support = build_checker.is_support(build)
    tree = poe_tree_codec.codec.decode_url(build.tree)
    keystones = tree.get_keystones(poe_tree_codec.codec.keystones)

    embed = create_embed(author, build.level, build.ascendency_name, build.class_name,
                         build.get_active_skill(), is_support)
    # add new fields
    general_str = general_output.get_defense_string(build, keystones)
    if general_str:
        embed.add_field(name="General", value=general_str, inline=minified)

    key, offense = offense_output.get_offense(build, consts)
    if offense:
        embed.add_field(name=key, value=offense,
                        inline=minified)

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
    info_text = ""
    if pastebin:
        info_text += "[Pastebin](https://pastebin.com/{}) | ".format(pastebin)

    info_text += "[Web Tree]({}) | [**Web Preview**](https://poe.technology/poebuddy/{}) - created in [Path of Building](https://github.com/Openarl/PathOfBuilding). ".format(
        build.tree, pastebin)
    embed.add_field(name='Info:', value=info_text)

    return embed
