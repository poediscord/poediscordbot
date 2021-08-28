from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.poe_data import build_checker
from poediscordbot.cogs.pob.poe_data.poe_consts import show_avg_dps_skills
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds
from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.pob_xml_parser.models.skill import Skill


class OffenseAggregatorV2(AbstractAggregator):

    def __init__(self, build: Build, non_dps_skills):
        super().__init__(build)
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
                               build.get_player_stat('CombinedAvg', default_val=0)]

        self.ignite_dps = build.get_player_stat('IgniteDPS')

        self.max_player_dps = max(self.player_dps_list)
        self.max_minion_dps = max(self.minion_dps_list)
        self.max_avg_dps = max(self.comparison_avg)
        self.full_dps = max(self.full_dps_list)

        self.included_skills = build.get_active_gem_from_included_skills()

    def get_max_dps(self):
        return max(self.max_player_dps, self.max_minion_dps, self.ignite_dps or 0)

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
        if avg_dps:
            return 'Average Damage', self._generate_avg_dmg_output()
        elif full_dps:
            return 'Full DPS', self._generate_full_dps_output(minion)
        elif minion:
            return 'Minion Offense', self._generate_minion_output()
        elif player_dps:
            return 'DPS', self._generate_player_dps_output()
        elif self.ignite_dps:
            return 'Ignite', self._generate_player_ignite_output()
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

        output = f'**AVG**: {self.max_avg_dps:,.0f}\n'
        if self.ignite_dps and self.ignite_dps > self.max_avg_dps * speed:
            output += f'**Ignite DPS**: {self.ignite_dps:,.0f}\n'
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

        return self.__generate_dps_string(total_dps, speed, impale_dps, ignite_dps) \
               + self.__generate_crit_acc_string(crit_chance, crit_multi, acc)

    def _generate_player_dps_output(self):
        speed = self.build.get_player_stat('Speed')
        impale_dps = self.build.get_player_stat('ImpaleDPS')
        total_dps = self.max_player_dps
        crit_chance = self.build.get_player_stat('CritChance', )
        crit_multi = self.build.get_player_stat('CritMultiplier')
        acc = self.build.get_player_stat('HitChance')

        return self.__generate_dps_string(total_dps, speed, impale_dps, self.ignite_dps) \
               + self.__generate_crit_acc_string(crit_chance, crit_multi, acc)

    def _generate_full_dps_output(self, minion_stats=False):
        crit_chance = self.build.get_player_stat('CritChance') if not minion_stats else self.build.get_minion_stat('CritChance')
        crit_multi = self.build.get_player_stat('CritMultiplier') if not minion_stats else self.build.get_minion_stat('CritMultiplier')
        acc = self.build.get_player_stat('HitChance') if not minion_stats else self.build.get_minion_stat('HitChance')
        gem_breakdown = ', '.join([f'{gem.get_name()} × {gem.instance_count}' for gem in self.included_skills])

        return f'**Combined DPS**: {self.full_dps:,.0f}\n ' + self.__generate_crit_acc_string(crit_chance, crit_multi,
                                                                                              acc) \
               + f' **Sources**: {gem_breakdown}'

    def _generate_player_ignite_output(self):
        return f'**Ignite DPS**: {self.ignite_dps:,.0f}'

    @staticmethod
    def __generate_dps_string(total_dps, speed, impale_dps=None, ignite_dps=None):
        output = ''
        output += f'**Total DPS**: {total_dps:,.0f}'
        if speed and speed > 0:
            output += f' @ {round(speed, 2) if speed else 0}/s\n'
        if impale_dps and impale_dps > total_dps * OutputThresholds.IMPALE_DPS_RATIO.value:
            output += f'**Impale DPS**: {impale_dps:,.0f}\n'
        if ignite_dps and ignite_dps > total_dps:
            output += f'**Ignite DPS**: {ignite_dps:,.0f}\n'
        return output

    @staticmethod
    def __generate_crit_acc_string(crit_chance=None, crit_multi=None, accuracy=None):
        output = ''
        if crit_chance and crit_chance > OutputThresholds.CRIT_CHANCE.value:
            output += f'**Crit**: Chance {crit_chance:,.2f}%' \
                      f', Multiplier: {crit_multi * 100 if crit_multi else 150:,.0f}%\n'
        if accuracy and accuracy < OutputThresholds.ACCURACY.value:
            output += f' **Hit Chance**: {accuracy:.2f}%'
        return output