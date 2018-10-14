from src.bot.consts.thresholds import OutputThresholds

from src.models import Build
from util import poe_consts


def is_support(build: Build, dps=0, avg=0):
    return (dps < OutputThresholds.DPS_SUPPORT.value and avg < OutputThresholds.AVG_SUPPORT.value) \
           and (build.aura_count > OutputThresholds.AURA_SUPPORT.value \
                or build.curse_count > OutputThresholds.CURSE_SUPPORT.value)


def has_offensive_ability(build: Build):
    skill = build.get_active_skill().get_selected()
    if skill and (skill.name in poe_consts.aura_list
                  or skill.name in poe_consts.curse_list
                  or skill.name in poe_consts.utility_skills):
        return False
    return True
