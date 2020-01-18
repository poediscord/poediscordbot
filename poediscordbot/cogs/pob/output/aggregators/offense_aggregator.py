from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.poe_data import build_checker
from poediscordbot.cogs.pob.poe_data.poe_consts import show_avg_dps_skills
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
                show_avg = show_avg or gem_name.lower() in show_avg_dps_skills

            return show_avg

    @staticmethod
    def _get_damage_output(build, avg, player_dps, minion_dps, ignite_dps):
        output = ""
        player_speed = build.get_player_stat('Speed')
        minion_speed = build.get_minion_stat('Speed')

        if OffenseAggregator.show_avg_damage(build.get_active_skill()) or avg > max(player_dps, minion_dps):
            output += f"**AVG**: {avg:,.0f}\n"
        elif player_dps > minion_dps:
            output += f"**DPS**: {player_dps:,.0f}"
            if player_speed > 0:
                output += f"@ {round(player_speed, 2) if player_speed else 0}/s\n"
        elif minion_dps > player_dps:
            output += f"**DPS**: {minion_dps:,.0f}"
            if minion_speed > 0:
                output += f"@ {round(minion_speed, 2) if minion_speed else 0}/s\n"
        elif ignite_dps > player_dps or (avg and ignite_dps > avg * player_speed):
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
        player_dps_list = [build.get_player_stat('TotalDPS'), build.get_player_stat('WithPoisonDPS'),
                           build.get_player_stat('WithImpaleDPS'), build.get_player_stat('BleedDPS')]
        minion_dps_list = [build.get_minion_stat('TotalDPS'), build.get_minion_stat('WithPoisonDPS'),
                           build.get_minion_stat('WithImpaleDPS')]
        comparison_avg = [build.get_player_stat('WithPoisonAverageDamage'), build.get_player_stat("AverageDamage")]
        player_dps = max([dps if dps else 0 for dps in player_dps_list])
        minion_dps = max([dps if dps else 0 for dps in minion_dps_list])
        ignite_dps = build.get_player_stat('IgniteDPS')
        player_avg = self.calc_max(comparison_avg)

        if build_checker.is_support(build, max(player_dps, minion_dps), player_avg):
            return "Support", self._get_support_output(build)
        else:
            return "Offense", self._get_damage_output(build, player_avg, player_dps, minion_dps,
                                                      0 if not ignite_dps else ignite_dps)