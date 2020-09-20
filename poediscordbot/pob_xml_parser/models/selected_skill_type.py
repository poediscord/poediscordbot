from enum import Enum

from poediscordbot.cogs.pob.poe_data.poe_consts import show_avg_dps_skills
from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.pob_xml_parser.models.skill import Skill


class SelectedSkillType(Enum):
    MINION_DPS = "minion_dps",
    AVG = "avg",
    DPS = "dps"
    IMPALE_DPS = "impale_dps"

    def getType(self, build: Build):
        if self.show_avg_damage(build.get_active_skill()):
            return self.AVG

    @staticmethod
    def show_avg_damage(active_skill: Skill) -> bool:
        """
        Determine if we have to show avg damage instead of dps (useful for mines and traps)
        :return: boolean
        """
        if active_skill:
            selected_skill = active_skill.get_selected()
            show_avg = any("mine" in gem.get_name().lower() for gem in active_skill.gems if gem.get_name())
            show_avg = show_avg or any(
                "trap" in gem.get_name().lower() for gem in active_skill.gems if gem.get_name())
            if selected_skill and selected_skill.get_name():
                gem_name = selected_skill.get_name()
                show_avg = show_avg or gem_name.lower() in show_avg_dps_skills

            return show_avg
