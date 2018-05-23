from src.bot.consts.thresholds import OutputThresholds

from src.models import Build


def is_support(build: Build):
    return build.aura_count > OutputThresholds.AURA_SUPPORT.value or build.curse_count > OutputThresholds.CURSE_SUPPORT.value
