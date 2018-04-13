from bot.consts.thresholds import OutputThresholds


def calc_dps(comparison_dps: []):
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


def get_offense(build):
    output = ""
    # Basics
    comparison_dps = [build.get_stat('Player', 'TotalDPS'), build.get_stat('Player', 'WithPoisonDPS'),
                      build.get_stat('Minion', 'TotalDPS'), build.get_stat('Minion', 'WithPoisonDPS')]

    dps = calc_dps(comparison_dps)
    if dps > 0:
        speed = build.get_stat('Player','Speed')
        output += "**DPS**: {dps:,.0f} @ {speed}/s\n".format(
            dps=dps,
            speed=round(speed, 2) if speed else 0)

        crit_chance = build.get_stat('Player','CritChance',)
        crit_multi = build.get_stat('Player','CritMultiplier')
        print(crit_multi)
        if crit_chance and crit_chance > OutputThresholds.CRIT_CHANCE.value:
            output += "**Crit**: Chance {crit_chance:,.2f}% | Multiplier: {crit_multi:,.0f}%\n".format(
                crit_chance=crit_chance,
                crit_multi=crit_multi*100 if crit_multi else 150)

        acc = build.get_stat('Player','HitChance',)

        if acc and acc < OutputThresholds.ACCURACY.value:
            output += "**Hit Chance**: {:.2f}%".format(acc)

        # todo: make a toggle for dot/hits
        return output
