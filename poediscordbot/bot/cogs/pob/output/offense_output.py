from poediscordbot.bot.cogs.pob.build import build_checker
from poediscordbot.bot.cogs.pob.build.thresholds import OutputThresholds
from poediscordbot.models import Skill


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
        selected_skill = active_skill.get_selected()
        show_avg = any("mine" in gem.get_name().lower() for gem in active_skill.gems if gem.get_name())
        show_avg = show_avg or any("trap" in gem.get_name().lower() for gem in active_skill.gems if gem.get_name())
        if selected_skill and selected_skill.get_name():
            gem_name = selected_skill.get_name()
            show_avg = show_avg or "firestorm" in gem_name.lower() \
                       or "ice storm" in gem_name.lower() \
                       or "molten burst" in gem_name.lower()

        return show_avg


def get_damage_output(build, avg, dps, ignite_dps):
    output = ""
    speed = build.get_stat('Player', 'Speed')
    minion_speed = build.get_stat('Minion', 'Speed')
    shown_speed = speed if not minion_speed or minion_speed < speed else minion_speed

    if show_avg_damage(build.get_active_skill()) or avg > dps:
        output += "**AVG**: {avg:,.0f}\n".format(
            avg=avg)
    else:
        output += "**DPS**: {dps:,.0f}".format(
            dps=dps)
        if shown_speed > 0:
            output += "@ {speed}/s\n".format(
                speed=round(shown_speed, 2) if shown_speed else 0)

    if ignite_dps > dps or (avg and ignite_dps > avg * shown_speed):
        output += "**Ignite DPS**: {ignite:,.0f}\n".format(
            ignite=ignite_dps
        )

    crit_chance = build.get_stat('Player', 'CritChance', )
    crit_multi = build.get_stat('Player', 'CritMultiplier')
    if crit_chance and crit_chance > OutputThresholds.CRIT_CHANCE.value:
        output += "**Crit**: Chance {crit_chance:,.2f}% | Multiplier: {crit_multi:,.0f}%\n".format(
            crit_chance=crit_chance,
            crit_multi=crit_multi * 100 if crit_multi else 150)

    acc = build.get_stat('Player', 'HitChance')

    if acc and acc < OutputThresholds.ACCURACY.value:
        output += "**Hit Chance**: {:.2f}%".format(acc)
    return output


def get_support_outptut(build):
    return "Auras: {}, Curses: {}".format(build.aura_count, build.curse_count)


def get_offense(build, consts=None):
    """
    Parses the meat of the build as in either support or dmg stats
    :param build:  Build instance
    :return: String (Support|Offense), String (Output)
    """
    if not build_checker.has_offensive_ability(build, consts):
        return "None", None

    # Basics
    comparison_dps = [build.get_stat('Player', 'TotalDPS'), build.get_stat('Player', 'WithPoisonDPS'),
                      build.get_stat('Minion', 'TotalDPS'), build.get_stat('Minion', 'WithPoisonDPS')]
    comparison_avg = [build.get_stat('Player', 'WithPoisonAverageDamage'), build.get_stat("Player", "AverageDamage")]
    dps = calc_max(comparison_dps)
    ignite_dps = build.get_stat('Player', 'IgniteDPS')
    avg = calc_max(comparison_avg)
    if build_checker.is_support(build, dps, avg):
        return "Support", get_support_outptut(build)
    else:
        return "Offense", get_damage_output(build, avg, dps, 0 if not ignite_dps else ignite_dps)
