from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.pob_xml_parser.models.skill import Skill


class SkillAggregator(AbstractAggregator):
    def get_output(self) -> (str, str):
        return 'Skill', self._get_main_skill(self.build)

    @staticmethod
    def _get_main_skill(build):
        active_skill = build.get_active_skill()
        if active_skill and isinstance(active_skill, Skill):
            output = active_skill.get_links(item=build.get_item(active_skill.slot))
            return output
        else:
            return "None selected"
