from enum import Enum

from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds
from poediscordbot.pob_xml_parser.models.build import Build


class GeneralStats(Enum):
    LIFE = 'Life'
    MANA = 'Mana'
    ENERGY_SHIELD = "Energy Shield"


class GeneralAggregator(AbstractAggregator):

    def __init__(self, build: Build, stat: GeneralStats):
        super().__init__(build)
        self.stat = stat

    def get_output(self) -> (str, str):
        return self.stat.value, self._get_defense_string(self.build, self.stat)

    @staticmethod
    def _get_basic_line(stat, stat_percent, stat_unreserved=0, stat_regen=0, stat_leech_rate=0, net_regen=None):
        output = None
        if isinstance(stat, float) and stat > 0 and isinstance(stat_percent, float):
            output = "**Amount**: "
            if stat_unreserved and stat - stat_unreserved > 0:
                output += f"{stat_unreserved:,.0f}/"
            output += f"{stat:,.0f}"
            output += f" ({stat_percent:,.0f}%)"
            if stat_regen:
                # Total regen, if displayed is regen - degen.
                net_regen_str = f'{net_regen:,.0f}/' if net_regen else None
                output += f'\n **Reg**: {net_regen_str or ""}{stat_regen:,.0f}/s ({stat_regen / stat * 100:,.0f}%)'
            if stat_leech_rate:
                output += f'\n **Leech** {stat_leech_rate:,.0f}/s ({stat_leech_rate / stat * 100:,.0f}%)'
        return output

    def _get_defense_string(self, build: Build, stat: GeneralStats):

        if stat is GeneralStats.LIFE:
            net_regen = build.get_player_stat('NetLifeRegen')
            life_percent_threshold = min(OutputThresholds.LIFE_PERCENT.value,
                                         OutputThresholds.LIFE_PERCENT_PER_LEVEL.value * build.level)
            life_flat = build.get_player_stat('Life')
            life_leech_threshold = life_flat * OutputThresholds.LEECH.value if life_flat else 0
            return self._get_basic_line(life_flat,
                                        build.get_player_stat('Spec:LifeInc', life_percent_threshold),
                                        stat_regen=build.get_player_stat('LifeRegen'),
                                        stat_unreserved=build.get_player_stat('LifeUnreserved'),
                                        stat_leech_rate=build.get_player_stat('LifeLeechGainRate',
                                                                              life_leech_threshold),
                                        net_regen=net_regen)

        if stat is GeneralStats.ENERGY_SHIELD:
            es_percent_threshold = min(OutputThresholds.ES_PERCENT.value,
                                       OutputThresholds.ES_PERCENT_PER_LEVEL.value * build.level)
            es_flat = build.get_player_stat('EnergyShield')
            es_leech_threshold = es_flat * OutputThresholds.LEECH.value if es_flat else 0
            return self._get_basic_line(es_flat,
                                        build.get_player_stat('Spec:EnergyShieldInc', es_percent_threshold),
                                        stat_regen=build.get_player_stat('EnergyShieldRegen'),
                                        stat_leech_rate=build.get_player_stat('EnergyShieldLeechGainRate',
                                                                              es_leech_threshold))
        if stat is GeneralStats.MANA:
            mana_flat = build.get_player_stat('Mana')
            mana_leech_threshold = mana_flat * OutputThresholds.LEECH.value if mana_flat else 0
            return self._get_basic_line(mana_flat, build.get_player_stat('Spec:ManaInc'),
                                        stat_regen=build.get_player_stat('ManaRegen'),
                                        stat_unreserved=build.get_player_stat('ManaUnreserved'),
                                        stat_leech_rate=build.get_player_stat('ManaLeechGainRate',
                                                                              mana_leech_threshold))
