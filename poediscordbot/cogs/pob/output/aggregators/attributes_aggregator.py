from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds


class AttributesAggregator(AbstractAggregator):

    def get_output(self) -> (str, str):
        return 'Attributes', self._get_attributes(self.build.get_player_stat('Str'), self.build.get_player_stat('Int'),
                                                  self.build.get_player_stat('Dex'))

    def _get_attributes(self, strength, intelligence, dexterity):
        """
        Display the attribute values if either of them meets the threshold defined in ~OutputThresholds.ATTRIBUTES
        :param strength: float value player strength
        :param intelligence: float value player intelligence
        :param dexterity: float value player dexterity
        :return: combined attributes string for embed usage
        """
        output = "**Attributes**: "
        if not strength:
            strength = 0
        if not intelligence:
            intelligence = 0
        if not dexterity:
            dexterity = 0

        if strength > OutputThresholds.ATTRIBUTES.value \
                or intelligence > OutputThresholds.ATTRIBUTES.value \
                or dexterity > OutputThresholds.ATTRIBUTES.value:
            return output + f"Str: {self.format_attribute(strength)}" \
                   + f" Int: {self.format_attribute(intelligence)}" \
                   + f" Dex: {self.format_attribute(dexterity)}\n"

    @staticmethod
    def format_attribute(attribute):
        """
        If an attribute is above or equal to the threshold mark it in bold
        :param attribute: to mark up
        :return: bold or nonbold integer value of the attribute (rounded)
        """
        if attribute >= OutputThresholds.ATTRIBUTES.value:
            return f"**{attribute:.0f}**"
        else:
            return f"{attribute:.0f}"
