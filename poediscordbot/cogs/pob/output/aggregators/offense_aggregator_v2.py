from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.poe_data import build_checker
from poediscordbot.cogs.pob.poe_data.poe_consts import show_avg_dps_skills
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds
from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.pob_xml_parser.models.skill import Skill
from poediscordbot.util import shorten_number_string


class OffenseAggregatorV2(AbstractAggregator):
    minified = True

    def __init__(self, build: Build, non_dps_skills, decimals=1):
        super().__init__(build)
        self.decimals = decimals
        self.non_dps_skills = non_dps_skills

        self.full_dps_list = [build.get_minion_stat('FullDPS', default_val=0),
                              build.get_player_stat("FullDPS", default_val=0)]

        self.player_dps_list = [build.get_player_stat('TotalDPS', default_val=0),
                                build.get_player_stat('WithPoisonDPS', default_val=0),
                                build.get_player_stat('WithImpaleDPS', default_val=0),
                                build.get_player_stat('BleedDPS', default_val=0),
                                build.get_player_stat('CombinedDPS', default_val=0)]
        self.minion_dps_list = [build.get_minion_stat('TotalDPS', default_val=0),
                                build.get_minion_stat('WithPoisonDPS', default_val=0),
                                build.get_minion_stat('WithImpaleDPS', default_val=0)]
        self.comparison_avg = [build.get_player_stat('WithPoisonAverageDamage', default_val=0),
                               build.get_player_stat('AverageDamage', default_val=0),
                               build.get_player_stat('AverageHit', default_val=0),
                               build.get_player_stat('CombinedAvg', default_val=0)]

        self.total_dot_dps = build.get_player_stat('TotalDotDPS')

        self.max_player_dps = max(self.player_dps_list)
        self.max_minion_dps = max(self.minion_dps_list)
        self.max_avg_dps = max(self.comparison_avg)
        self.full_dps = max(self.full_dps_list)

        self.included_skills = build.get_active_gem_from_included_skills()

    def get_max_dps(self):
        return max(self.max_player_dps, self.max_minion_dps, self.total_dot_dps or 0)

    def get_avg_dps(self):
        return self.max_avg_dps

    def get_output(self) -> (str, str):
        if not build_checker.has_offensive_ability(self.build, self.non_dps_skills):
            return 'None', None

        avg_dps = self.show_avg_damage(self.build.get_active_skill())
        full_dps = self.full_dps > self.max_player_dps and self.full_dps > self.max_player_dps
        minion = self.max_minion_dps > self.max_player_dps
        player_dps = self.max_player_dps > self.max_minion_dps

        if build_checker.is_support(self.build, self.get_max_dps(),
                                    self.get_avg_dps()):
            return 'Support', self._get_support_output()
        elif self.total_dot_dps and self.total_dot_dps > self.max_avg_dps:
            return 'DOT', self._generate_player_dot_output()
        if avg_dps:
            return 'Average Damage', self._generate_avg_dmg_output()
        elif full_dps:
            return 'Full DPS', self._generate_full_dps_output(minion)
        elif minion:
            return 'Minion Offense', self._generate_minion_output()
        elif player_dps:
            return 'DPS', self._generate_player_dps_output()
        else:
            return 'DPS', None

    @staticmethod
    def show_avg_damage(active_skill: Skill) -> bool:
        """
        Determine if we have to show avg damage instead of dps (useful for mines and traps)
        :return: boolean
        """
        if active_skill:
            selected_skill = active_skill.get_selected()
            show_avg = any('mine' in gem.get_name().lower() for gem in active_skill.gems if gem.get_name())
            show_avg = show_avg or any('trap' in gem.get_name().lower() for gem in active_skill.gems if gem.get_name())
            if selected_skill and selected_skill.get_name():
                gem_name = selected_skill.get_name()
                show_avg = show_avg or gem_name.lower() in show_avg_dps_skills

            return show_avg

    def _get_support_output(self):
        return f'Auras: {self.build.aura_count}, Curses: {self.build.curse_count}'

    def _generate_avg_dmg_output(self):
        crit_chance = self.build.get_player_stat('CritChance', )
        crit_multi = self.build.get_player_stat('CritMultiplier')
        acc = self.build.get_player_stat('HitChance')
        speed = self.build.get_player_stat('Speed')

        output = f'**AVG**: {shorten_number_string(self.max_avg_dps, decimals=self.decimals)}\n'
        if self.total_dot_dps and self.total_dot_dps > self.max_avg_dps * speed:
            output += f'**DoT DPS**: {shorten_number_string(self.total_dot_dps, decimals=self.decimals)}\n'
        output += self.__generate_crit_acc_string(crit_chance, crit_multi, acc)
        return output

    def _generate_minion_output(self):
        speed = self.build.get_minion_stat('Speed')
        impale_dps = self.build.get_minion_stat('ImpaleDPS')
        total_dps = self.max_minion_dps
        crit_chance = self.build.get_minion_stat('CritChance')
        crit_multi = self.build.get_minion_stat('CritMultiplier')
        acc = self.build.get_minion_stat('HitChance')
        ignite_dps = self.build.get_minion_stat('IgniteDPS')

        return self.__generate_dps_string(total_dps, speed, self.decimals, impale_dps, ignite_dps) \
               + self.__generate_crit_acc_string(crit_chance, crit_multi, acc)

    def _generate_player_dps_output(self):
        speed = self.build.get_player_stat('Speed')
        impale_dps = self.build.get_player_stat('ImpaleDPS')
        total_dps = self.max_player_dps
        crit_chance = self.build.get_player_stat('CritChance', )
        crit_multi = self.build.get_player_stat('CritMultiplier')
        acc = self.build.get_player_stat('HitChance')

        return self.__generate_dps_string(total_dps, speed, self.decimals, impale_dps, self.total_dot_dps) \
               + self.__generate_crit_acc_string(crit_chance, crit_multi, acc)

    def _generate_full_dps_output(self, minion_stats=False):
        crit_chance = self.build.get_player_stat('CritChance') if not minion_stats else self.build.get_minion_stat(
            'CritChance')
        crit_multi = self.build.get_player_stat('CritMultiplier') if not minion_stats else self.build.get_minion_stat(
            'CritMultiplier')
        acc = self.build.get_player_stat('HitChance') if not minion_stats else self.build.get_minion_stat('HitChance')
        gem_breakdown = ', '.join([f'{gem.get_name()} × {gem.instance_count}' for gem in self.included_skills])

        return f'**Combined DPS**: {shorten_number_string(self.full_dps, decimals=self.decimals)}\n ' + self.__generate_crit_acc_string(
            crit_chance, crit_multi, acc) + f' **Sources**: {gem_breakdown}'

    def _generate_player_dot_output(self):
        return f'**Total DPS**: {shorten_number_string(self.total_dot_dps, decimals=self.decimals)}'

    @staticmethod
    def __generate_dps_string(total_dps, speed, decimals, impale_dps=None, ignite_dps=None):
        output = ''
        output += f'**Total DPS**: {shorten_number_string(total_dps, decimals=decimals)}'
        if speed and speed > 0:
            output += f' @ {round(speed, 2) if speed else 0}/s\n'
        if impale_dps and impale_dps > total_dps * OutputThresholds.IMPALE_DPS_RATIO.value:
            output += f'**Impale DPS**: {shorten_number_string(impale_dps, decimals=decimals)}\n'
        if ignite_dps and ignite_dps > total_dps:
            output += f'**Ignite DPS**: {shorten_number_string(ignite_dps, decimals=decimals)}\n'
        return output

    @staticmethod
    def __generate_crit_acc_string(crit_chance=None, crit_multi=None, accuracy=None):
        output = ''
        if crit_chance and crit_chance > OutputThresholds.CRIT_CHANCE.value:
            output += f'**Crit**: {crit_chance:,.2f}%' \
                      f', Multi: {crit_multi * 100 if crit_multi else 150:,.0f}%\n'
        if accuracy and accuracy < OutputThresholds.ACCURACY.value:
            output += f' **Hit Chance**: {accuracy:.2f}%'
        return output
