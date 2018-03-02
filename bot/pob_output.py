import logging

from defusedxml import ElementTree
from discord import Embed

import config
from models import Build
from util.poeurl import shrink_tree_url
from bot.parser import Parser


def get_md_codeblock(string):
    return '```css\n' + string + '```'


def create_embed(author, tree, level, ascendency_name, class_name, main_skill="UNDEFINED"):
    embed = Embed(title='tmp', color=config.color)

    if ascendency_name and ascendency_name != "":
        embed.set_thumbnail(
            url='http://web.poecdn.com/image/Art/2DArt/SkillIcons/passives/Ascendants/' + ascendency_name + '.png')

    embed.title = "{gem} - {char} (Lvl: {level})".format(
        char=class_name if ascendency_name.lower() == 'none' else ascendency_name,
        gem=main_skill,
        level=level)
    if author:
        embed.title += " by " + author.name
    return embed


def generate_block(embed, data_dict):
    for val in data_dict:
        pass


def generate_output(author, build: Build):
    print(author)

    embed = create_embed(author, build.tree, build.level, build.ascendency_name, build.class_name, build.get_active_skill())
    # add stuff

    # output
    embed.add_field(name='Tree:', value=build.tree, inline=False)
    return embed
