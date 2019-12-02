from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.poe_data import build_checker
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds
from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.pob_xml_parser.models.skill import Skill


class OffenseAggregator(AbstractAggregator):

    def __init__(self, build: Build, non_dps_skills):
        super().__init__(build)
        self.non_dps_skills = non_dps_skills

    def get_output(self) -> (str, str):
        return self.get_offense_or_support_string(self.build, self.non_dps_skills)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def _get_damage_output(build, avg, dps, ignite_dps):
        output = ""
        speed = build.get_player_stat('Speed')
        minion_speed = build.get_minion_stat('Speed')
        shown_speed = speed if not minion_speed or minion_speed < speed else minion_speed

        if OffenseAggregator.show_avg_damage(build.get_active_skill()) or avg > dps:
            output += f"**AVG**: {avg:,.0f}\n"
        else:
            output += f"**DPS**: {dps:,.0f}"
            if shown_speed > 0:
                output += f"@ {round(shown_speed, 2) if shown_speed else 0}/s\n"

        if ignite_dps > dps or (avg and ignite_dps > avg * shown_speed):
            output += f"**Ignite DPS**: {ignite_dps:,.0f}\n"

        crit_chance = build.get_player_stat('CritChance', )
        crit_multi = build.get_player_stat('CritMultiplier')
        if crit_chance and crit_chance > OutputThresholds.CRIT_CHANCE.value:
            output += f"**Crit**: Chance {crit_chance:,.2f}%" \
                f" | Multiplier: {crit_multi * 100 if crit_multi else 150:,.0f}%\n"

        acc = build.get_player_stat('HitChance')

        if acc and acc < OutputThresholds.ACCURACY.value:
            output += f"**Hit Chance**: {acc:.2f}%"
        return output

    @staticmethod
    def _get_support_output(build):
        return f"Auras: {build.aura_count}, Curses: {build.curse_count}"

    def get_offense_or_support_string(self, build, consts=None):
        """
        Parses the meat of the poe_data as in either support or dmg stats
        :param consts:
        :param build:  Build instance
        :return: String (Support|Offense), String (Output)
        """
        if not build_checker.has_offensive_ability(build, consts):
            return "None", None

        # Basics
        comparison_dps = [build.get_player_stat('TotalDPS'), build.get_player_stat('WithPoisonDPS'),
                          build.get_minion_stat('TotalDPS'), build.get_minion_stat('WithPoisonDPS')]
        comparison_avg = [build.get_player_stat('WithPoisonAverageDamage'), build.get_player_stat("AverageDamage")]
        dps = self.calc_max(comparison_dps)
        ignite_dps = build.get_player_stat('IgniteDPS')
        avg = self.calc_max(comparison_avg)
        if build_checker.is_support(build, dps, avg):
            return "Support", self._get_support_output(build)
        else:
            return "Offense", self._get_damage_output(build, avg, dps, 0 if not ignite_dps else ignite_dps)
