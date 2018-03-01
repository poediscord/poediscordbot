from defusedxml import ElementTree
from discord import Embed

from models import Build, PlayerStat


def decode_build(build):
    """
    Decodes all build information and playerstats into the specific model we expect.
    :param build:
    :return:
    """
    build_info = Build(build.attrib['level'], build.attrib['targetVersion'], build.attrib['bandit'],
                       build.attrib['className'],
                       build.attrib['ascendClassName'])
    for player_stat in build:
        build_info.appendStat(PlayerStat(player_stat.attrib['stat'], player_stat.attrib['value']))
    return build_info


def embed_message(build=None, author=None):
    embed = Embed(title='PoB Discord', color=0x0433ff)
    print(type(build))
    if build and isinstance(build, Build):
        embed.add_field(name='Build', value='```css\n' + build.to_string() + '```')
        if build.ascendencyName and build.ascendencyName != "":
            embed.set_thumbnail(
                url='http://web.poecdn.com/image/Art/2DArt/SkillIcons/passives/Ascendants/' + build.ascendencyName + '.png')

    embed.title = "Random"  # todo: set this to version + class|asc + skill
    if author:
        embed.title += " - by " + author.name
    return embed


def generate_output(author, pob_xml: ElementTree):
    print(author)
    build = pob_xml.find('Build')

    build = decode_build(build)
    ret = embed_message(author=author, build=build)
    return ret
