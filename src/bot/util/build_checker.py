from src.bot.consts.thresholds import OutputThresholds

from src.models import Build


def is_support(build: Build, dps=0, avg=0):
    return (dps < OutputThresholds.DPS_SUPPORT.value or avg < OutputThresholds.AVG_SUPPORT.value) \
           and (build.aura_count > OutputThresholds.AURA_SUPPORT.value \
                or build.curse_count > OutputThresholds.CURSE_SUPPORT.value)
