from src.bot.consts.thresholds import OutputThresholds
from src.bot.util import build_checker
from src.models import Skill


def calc_max(comparison_dps: []):
    """
    Get the max value out of all values in the list when they are set.
    :param comparison_dps:
    :return:
    """
    max = 0
    for dps in comparison_dps:
        if dps and dps > max:
            max = dps
    return round(max, 2)


def show_avg_damage(active_skill: Skill) -> bool:
    """
    Determine if we have to show avg damage instead of dps (useful for mines and traps)
    :return: boolean
    """
    if active_skill:
        show_avg = any("mine" in gem.get_name().lower() for gem in active_skill.gems)
        show_avg = show_avg or any("trap" in gem.get_name().lower() for gem in active_skill.gems)
        selected_skill = active_skill.get_selected().get_name()
        show_avg = show_avg or "firestorm" in selected_skill.lower() or "ice storm" in selected_skill.lower()

        return show_avg


def get_damage_output(build, avg, dps):
    output = ""
    speed = build.get_stat('Player', 'Speed')
    minion_speed = build.get_stat('Minion', 'Speed')
    if show_avg_damage(build.get_active_skill()) or avg > dps:
        output += "**AVG**: {avg:,.0f}\n".format(
            avg=avg)
    else:
        shown_speed = speed if not minion_speed or minion_speed < speed else minion_speed
        output += "**DPS**: {dps:,.0f} @ {speed}/s\n".format(
            dps=dps,
            speed=round(shown_speed, 2) if shown_speed else min)

    crit_chance = build.get_stat('Player', 'CritChance', )
    crit_multi = build.get_stat('Player', 'CritMultiplier')
    if crit_chance and crit_chance > OutputThresholds.CRIT_CHANCE.value:
        output += "**Crit**: Chance {crit_chance:,.2f}% | Multiplier: {crit_multi:,.0f}%\n".format(
            crit_chance=crit_chance,
            crit_multi=crit_multi * 100 if crit_multi else 150)

    acc = build.get_stat('Player', 'HitChance', )

    if acc and acc < OutputThresholds.ACCURACY.value:
        output += "**Hit Chance**: {:.2f}%".format(acc)
    return output


def get_support_outptut(build):
    return "Auras: {}, Curses: {}".format(build.aura_count, build.curse_count)


def get_offense(build):
    """
    Parses the meat of the build as in either support or dmg stats
    :param build:  Build instance
    :return: String (Support|Offense), String (Output)
    """
    output = ""
    # Basics
    comparison_dps = [build.get_stat('Player', 'TotalDPS'), build.get_stat('Player', 'WithPoisonDPS'),
                      build.get_stat('Minion', 'TotalDPS'), build.get_stat('Minion', 'WithPoisonDPS')]
    comparison_avg = [build.get_stat('Player', 'WithPoisonAverageDamage'), build.get_stat("Player", "AverageDamage")]
    dps = calc_max(comparison_dps)
    avg = calc_max(comparison_avg)
    if build_checker.is_support(build, dps, avg):
        return "Support", get_support_outptut(build)
    else:
        return "Offense", get_damage_output(build, avg, dps)
