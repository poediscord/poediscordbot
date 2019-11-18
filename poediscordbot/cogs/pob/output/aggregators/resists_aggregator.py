from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds
from poediscordbot.pob_xml_parser.models.build import Build


class ResistAggregator(AbstractAggregator):

    def get_output(self) -> (str, str):
        return 'Resistances', self._get_resistances(self.build)

    @staticmethod
    def _get_resistances(build: Build):
        """
        Creates the resistance string
        :param build: poe_data we want to output
        :return: string containing all resistances or and empty string if nothing is noteworthy
        """
        output = ""
        resistances = ['Fire', 'Cold', 'Lightning', 'Chaos']
        emojis = [':fire:', ':snowflake:', ':zap:', ':skull:']
        show = False
        for i, resist_type in enumerate(resistances):
            threshold = OutputThresholds.CHAOS_RES.value if resist_type == 'Chaos' else OutputThresholds.ELE_RES.value
            res_val = build.get_player_stat(resist_type + 'Resist', threshold)

            if res_val:
                output += f"{emojis[i]} {res_val:.0f} "
                show = True

        return output if show else ""
