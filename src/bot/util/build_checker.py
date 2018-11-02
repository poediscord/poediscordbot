from src.bot.consts.thresholds import OutputThresholds

from src.models import Build


def is_support(build: Build, dps=0, avg=0):
    return (dps < OutputThresholds.DPS_SUPPORT.value and avg < OutputThresholds.AVG_SUPPORT.value) \
           and (build.aura_count > OutputThresholds.AURA_SUPPORT.value
                or build.curse_count > OutputThresholds.CURSE_SUPPORT.value)


def has_offensive_ability(build: Build, consts):
    skill = build.get_active_skill().get_selected()
    if consts and skill and (skill.name in consts.aura_list
                             or skill.name in consts.curse_list
                             or skill.name in consts.utility_skills):
        return False
    return True
