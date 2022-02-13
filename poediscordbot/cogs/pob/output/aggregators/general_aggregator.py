from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds
from poediscordbot.pob_xml_parser.models.build import Build


class GeneralAggregator(AbstractAggregator):

    def get_output(self) -> (str, str):
        return 'Defenses', self._get_defense_string(self.build)

    @staticmethod
    def _get_basic_line(name, stat, stat_percent, stat_unreserved=0, stat_regen=0, stat_leech_rate=0) -> str:
        output = None
        if isinstance(stat, float) and stat > 0 and isinstance(stat_percent, float):
            output = "**" + name + "**: "
            if stat_unreserved and stat - stat_unreserved > 0:
                output += f"{stat_unreserved:,.0f}/"
            output += f"{stat:,.0f}"
            output += f" ({stat_percent:,.0f}%)"
            if stat_regen:
                # Total regen, if displayed is regen - degen.
                output += f" | Reg: {stat_regen:,.0f}/s ({stat_regen / stat * 100:,.1f}%)"
            if stat_leech_rate:
                output += f" | Leech {stat_leech_rate:,.0f}/s ({stat_leech_rate / stat * 100:,.1f}%)"
            output += "\n"
        return output

    @staticmethod
    def _get_resistances(build: Build):
        """
        Creates the resistance string
        :param build: poe_data we want to output
        :return: string containing all resistances or and empty string if nothing is noteworthy
        """
        output = "**Resistances**: "
        resistances = ['Fire', 'Cold', 'Lightning', 'Chaos']
        emojis = [':fire:', ':snowflake:', ':zap:', ':skull:']
        show = False
        for i, res in enumerate(resistances):
            res_val = build.get_player_stat(res + 'Resist', OutputThresholds.CHAOS_RES.value if res == 'Chaos'
            else OutputThresholds.ELE_RES.value)
            res_over_cap = build.get_player_stat(res + 'ResistOverCap')

            if res_val:
                output += emojis[i] + f" {res_val:.0f}"
                show = True
                if res_over_cap and res_over_cap > 0:
                    output += f"(+{res_over_cap:.0f}) "
                output += " "
        output += "\n"
        return output if show else ""

    def _get_defense_string(self, build: Build):
        output = ""

        ehp = build.get_player_stat('TotalEHP', 0)
        second_minimal_maxhit = build.get_player_stat('SecondMinimalMaximumHitTaken', 0)
        if ehp:
            output += f"**EHP**: {ehp:,.0f} | Effective Maximum hit Taken: {second_minimal_maxhit:,.0f}\n"

        life_percent_threshold = min(OutputThresholds.LIFE_PERCENT.value,
                                     OutputThresholds.LIFE_PERCENT_PER_LEVEL.value * build.level)
        life_flat = build.get_player_stat('Life')
        life_leech_rate = build.get_player_stat('LifeLeechGainRate',
                                                life_flat * OutputThresholds.LEECH.value if life_flat else 0)
        life_string = self._get_basic_line("Life", life_flat,
                                           build.get_player_stat('Spec:LifeInc', life_percent_threshold),
                                           stat_regen=build.get_player_stat('LifeRegen'),
                                           stat_unreserved=build.get_player_stat('LifeUnreserved'),
                                           stat_leech_rate=life_leech_rate)
        if life_string:
            output += life_string

        es_percent_threshold = min(OutputThresholds.ES_PERCENT.value,
                                   OutputThresholds.ES_PERCENT_PER_LEVEL.value * build.level)
        es_flat = build.get_player_stat('EnergyShield')
        harold_es_override = es_flat and es_flat > OutputThresholds.ES_FLAT.value

        if harold_es_override:
            es_percent_threshold = 0

        es_leech_rate = build.get_player_stat('EnergyShieldLeechGainRate',
                                              es_flat * OutputThresholds.LEECH.value if es_flat else 0)
        es_string = self._get_basic_line("Energy Shield", es_flat,
                                         build.get_player_stat('Spec:EnergyShieldInc', es_percent_threshold),
                                         stat_regen=build.get_player_stat('EnergyShieldRegen'),
                                         stat_leech_rate=es_leech_rate)
        if es_string:
            output += es_string

        ward = build.get_player_stat("Ward")
        if ward and ward > OutputThresholds.WARD.value:
            output += f"**Ward**: {ward:,.0f}\n"

        net_regen = build.get_player_stat('NetLifeRegen')

        if net_regen:
            output += f"**Net Regen**: {net_regen:,.0f}/s\n"
        mana_flat = build.get_player_stat('Mana')
        mana_leech_rate = build.get_player_stat('ManaLeechGainRate', mana_flat * OutputThresholds.LEECH.value if mana_flat else 0)
        mana_string = self._get_basic_line("Mana", mana_flat, build.get_player_stat('Spec:ManaInc'),
                                           stat_regen=build.get_player_stat('ManaRegen'),
                                           stat_unreserved=build.get_player_stat('ManaUnreserved'),
                                           stat_leech_rate=mana_leech_rate)
        if mana_string:
            output += mana_string

        output += self._get_resistances(build)
        return output
