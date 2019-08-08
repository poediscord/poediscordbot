from poediscordbot.pob_xml_parser.models import Skill


def get_main_skill(build):
    active_skill = build.get_active_skill()
    if active_skill and isinstance(active_skill, Skill):
        output = active_skill.get_links(item=build.get_item(active_skill.slot))
        return output
    else:
        return "None selected"
