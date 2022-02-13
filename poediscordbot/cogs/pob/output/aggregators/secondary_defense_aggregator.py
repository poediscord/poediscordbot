from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.cogs.pob.output.aggregators.attributes_aggregator import AttributesAggregator
from poediscordbot.cogs.pob.poe_data.thresholds import OutputThresholds
from poediscordbot.pob_xml_parser.models.build import Build


class SecondaryDefenseAggregator(AbstractAggregator):

    def get_output(self) -> (str, str):
        return 'Secondary Defense', self.get_secondary_defense_string(self.build)

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
        armour_inc = build.get_player_stat('Spec:ArmourInc', 0)
        stats.append(f"Armour: {armour:,.0f} ({armour_inc}%)") if armour and armour else None

        evasion = build.get_player_stat('Evasion', min(OutputThresholds.EVASION.value, effective_life))
        evasion_inc = build.get_player_stat('Spec:EvasionInc', 0)
        stats.append(f"Evasion: {evasion:,.0f} ({evasion_inc}%)") if evasion else None

        suppression = build.get_player_stat('SpellSuppressionChance', OutputThresholds.DODGE.value)
        stats.append(f"Spell Suppression: {suppression:,.0f}%") if suppression else None

        dodge = build.get_player_stat('AttackDodgeChance', OutputThresholds.DODGE.value)
        stats.append(f"Dodge: {dodge:,.0f}%") if dodge else None

        spell_dodge = build.get_player_stat('SpellDodgeChance', OutputThresholds.SPELL_DODGE.value)
        stats.append(f"Spell Dodge: {spell_dodge:,.0f}%") if spell_dodge else None

        block = build.get_player_stat('BlockChance', OutputThresholds.BLOCK.value)
        stats.append(f"Block: {block:,.0f}%") if block else None

        spell_block = build.get_player_stat('SpellBlockChance', OutputThresholds.SPELL_BLOCK.value)
        stats.append(f"Spell Block: {spell_block:,.0f}%") if spell_block else None

        total_move_speed = build.get_player_stat('EffectiveMovementSpeedMod', 2)
        if total_move_speed:
            movement_speed = (total_move_speed - 1) * 100
            stats.append(
                f"Movement Speed: {movement_speed:.0f}%") if movement_speed > OutputThresholds.MOVE_SPEED.value else None

        if len(stats) > 0:
            output += " | ".join([s for s in stats if s]) + "\n"
        return "**Secondary:** " + output if output != "" else None

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
            output += attributes

        if build.keystones:
            output += self._get_keystones(build.keystones)
        return output
