from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.output.aggregators.attributes_aggregator import AttributesAggregator
from poediscordbot.cogs.pob.output.aggregators.charges_aggregator import ChargesAggregator
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds
from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.util import shorten_number_string


class SecondaryDefenseAggregator(AbstractAggregator):
    minified = True

    def get_output(self) -> (str, str):
        return 'Stats', self.get_secondary_defense_string(self.build)

    def _get_secondary_def(self, build: Build):
        """
        Parse all secondary defenses such as armor, eva, dodge, block and display them if they are higher than the thresholds.
        :param build: current poe_data
        :return: String containing noteworthy secondary defense, Empty string as default
        """
        output = ""
        stats = []

        es = build.get_player_stat('EnergyShield')
        life = build.get_player_stat('Life')
        effective_life = life if life else 0
        if es and es > effective_life:
            effective_life = es

        armour = build.get_player_stat('Armour', min(OutputThresholds.ARMOUR.value, effective_life))
        stats.append(f"Armour: {shorten_number_string(armour)}\n") if armour and armour else None

        evasion = build.get_player_stat('Evasion', min(OutputThresholds.EVASION.value, effective_life))
        stats.append(f"Evasion: {shorten_number_string(evasion)}\n") if evasion else None

        suppression = build.get_player_stat('SpellSuppressionChance', OutputThresholds.DODGE.value)
        stats.append(f"Spell Supp: {shorten_number_string(suppression)}%\n") if suppression else None

        dodge = build.get_player_stat('AttackDodgeChance', OutputThresholds.DODGE.value)
        stats.append(f"Dodge: {shorten_number_string(dodge)}%\n") if dodge else None

        spell_dodge = build.get_player_stat('SpellDodgeChance', OutputThresholds.SPELL_DODGE.value)
        stats.append(f"Spell Dodge: {shorten_number_string(spell_dodge)}%\n") if spell_dodge else None

        block = build.get_player_stat('BlockChance', OutputThresholds.BLOCK.value)
        stats.append(f"Block: {shorten_number_string(block)}%\n") if block else None

        spell_block = build.get_player_stat('SpellBlockChance', OutputThresholds.SPELL_BLOCK.value)
        stats.append(f"Spell Block: {shorten_number_string(spell_block)}%\n") if spell_block else None

        total_move_speed = build.get_player_stat('EffectiveMovementSpeedMod', 2)
        if total_move_speed:
            movement_speed = (total_move_speed - 1) * 100
            stats.append(
                f"Movement Speed: {movement_speed:.0f}%\n") if movement_speed > OutputThresholds.MOVE_SPEED.value else None
        active_totem_limit = build.get_player_stat('ActiveTotemLimit', 0)
        if active_totem_limit > 2:
            stats.append(f"Totems: {active_totem_limit:.0f}\n")

        if len(stats) > 0:
            output += "".join([s for s in stats if s])
        return output if output != "" else None

    @staticmethod
    def _get_keystones(keystones: list, minified=False):
        keystone_strs = [keystone['name'] if not minified else keystone['abbrev'] for keystone in keystones]
        return "**Keystones**: " + ", ".join(keystone_strs)

    def get_secondary_defense_string(self, build: Build):
        output = ""

        secondary_def = self._get_secondary_def(build)
        if secondary_def:
            output += secondary_def

        _, attributes = AttributesAggregator(build).get_output()

        if attributes:
            output += f"{attributes}\n"

        _, charges = ChargesAggregator(build).get_output()

        if charges:
            output += f"**Charges**:\n{charges}\n"

        if build.keystones:
            output += self._get_keystones(build.keystones)
        return output
