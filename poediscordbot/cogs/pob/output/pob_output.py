from discord import Embed
from instance import config

from poediscordbot.cogs.pob.importers import PasteData
from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.output.aggregators.charges_aggregator import ChargesAggregator
from poediscordbot.cogs.pob.output.aggregators.config_aggregator import ConfigAggregator
from poediscordbot.cogs.pob.output.aggregators.general_aggregator import GeneralAggregator
from poediscordbot.cogs.pob.output.aggregators.offense_aggregator_v2 import OffenseAggregatorV2
from poediscordbot.cogs.pob.output.aggregators.secondary_defense_aggregator import SecondaryDefenseAggregator
from poediscordbot.cogs.pob.output.aggregators.skill_aggregator import SkillAggregator
from poediscordbot.cogs.pob.poe_data import build_checker
from poediscordbot.cogs.pob.util.pob import pob_minions
from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.pob_xml_parser.models.gem import Gem
from poediscordbot.pob_xml_parser.models.skill import Skill


def create_embed(author, level, ascendency_name, class_name, main_skill: Skill, is_support):
    """
    Create the basic embed we add information to
    :param author: of the parsed message - str
    :param level: of the poe_data
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
        gem_name = _fetch_displayed_skill(gem_name, main_skill)

    if ascendency_name or class_name:
        url = 'https://raw.github.com/poediscord/poediscordbot/master/resources/img/' + (
            ascendency_name if ascendency_name != "None" else class_name) + '.png'
        embed.set_thumbnail(url=url)
    class_display_name = class_name if ascendency_name.lower() == 'none' else ascendency_name
    embed.title = f"{gem_name} - {class_display_name} (Lvl: {level})"
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


def _fetch_displayed_skill(gem_name, main_skill):
    main_gem = main_skill.get_selected()
    if isinstance(main_gem, Gem):
        display_name = f'{main_gem.get_name()}'
        if display_name and main_gem.minion_skill and main_gem.selected_minion:
            monster_name = pob_minions.get_monster_name(main_gem.selected_minion, main_skill)
            if monster_name:
                display_name += f' ({monster_name})'
        return display_name
    else:
        return gem_name


def _generate_info_text(tree, paste_data, web_poe_token):
    info_text = ""
    if paste_data:
        info_text += f"[Build Link]({paste_data.source_url}) | "
    if tree and len(tree) < 600:
        info_text += f"[Web Tree]({tree}) "
    if web_poe_token:
        info_text += f"| [{config.web_pob_text}](https://pob.party/share/{web_poe_token}) "
    if paste_data and config.enable_open_in_pob_feature:
        info_text += f"| [Click to open in POB](https://fwidm.github.io/pob-redirect/index.html?{paste_data.source_site}={paste_data.key}). "
    info_text += f"\nCreated in [Path of Building: Community Fork](https://github.com/PathOfBuildingCommunity/PathOfBuilding). "
    return info_text


def expand_embed(embed: Embed, aggregator: AbstractAggregator, inline=False):
    key, val = aggregator.get_output()

    if key and val:
        embed.add_field(name=key, value=val, inline=inline)


def generate_response(author, build: Build, minified=False, paste_data: PasteData = None, non_dps_skills=None,
                      web_poe_token=None):
    """
    Build an embed to respond to the user.
    :param non_dps_skills: poe constants - skill info
    :param author: name of the person triggering the action
    :param build: poe_data to parse an embed from
    :param minified: (bool) whether to get a minified version or the full one
    :param paste_data: data about paste source
    :return: Filled embed for discord
    """

    # Needs to be created first because of embed support check
    offense_aggregator = OffenseAggregatorV2(build, non_dps_skills)
    is_support = build_checker.is_support(build,
                                          offense_aggregator.get_max_dps(),
                                          offense_aggregator.get_avg_dps())

    embed = create_embed(author, build.level, build.ascendancy_name, build.class_name,
                         build.get_active_skill(), is_support)

    base_aggregators = [
        GeneralAggregator(build),
        SecondaryDefenseAggregator(build),
        offense_aggregator,
        ChargesAggregator(build),
    ]
    additional_aggregators = [
        SkillAggregator(build),
        ConfigAggregator(build)
    ]

    [expand_embed(embed, aggregator, inline=minified) for aggregator in base_aggregators]

    if not minified:
        [expand_embed(embed, aggregator, inline=minified) for aggregator in additional_aggregators]

    # output
    embed.add_field(name='Info:', value=_generate_info_text(build.tree, paste_data, web_poe_token))

    if minified:
        embed.add_field(name='Hint:', value='Use `!pob <link to pastebin>` for even more build info!')

    return embed
