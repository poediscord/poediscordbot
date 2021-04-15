from poediscordbot.pob_xml_parser.models.gem import Gem


class Skill:
    __slots__ = 'gems', 'main_active_skill', 'slot', 'enabled', 'links', 'included_in_full_dps'

    def __init__(self, gems: [Gem], main_active_skill, slot=None, enabled=False, included_in_full_dps=False):
        self.slot = slot
        self.gems = gems
        self.enabled = True if enabled == 'true' else False
        self.main_active_skill = None

        if main_active_skill and main_active_skill.isdigit():
            self.main_active_skill = int(main_active_skill)

        self.links = len(gems)
        self.included_in_full_dps = included_in_full_dps

    def __repr__(self) -> str:
        return f"Skill [slot={self.slot}; gems={self.gems}; links={self.links}; selected={self.main_active_skill}; " \
               f"enabled={self.enabled}] "

    def get_active_gems(self):
        return [gem for gem in self.gems if gem.is_active]

    def get_selected(self) -> Gem:
        """
        Gets the selected main skill gem. first filter the this gem to only allow supports, then get the right gem
        via the main_active_skill.
        With new Vaal skills: Players can select the non vaal version in index+1 which is not saved in the xml.
        :return:
        """
        gem = None

        if self.main_active_skill:
            active_gems = [gem for gem in self.gems if gem.id and "support" not in gem.id.lower()]
            full_list = []
            # easier abstraction than calculating the stuff
            for gem in active_gems:
                if gem.name and 'vaal' in gem.name.lower():
                    full_list.append(gem)
                full_list.append(gem)
            if len(full_list) > 1:
                gem = full_list[self.main_active_skill - 1]
                # if the previous gem has the same name, toggle it to be the non val version.
                gem.set_active_part(1 if gem == full_list[self.main_active_skill - 2] else 0)
        return gem

    def get_links(self, item=None, join_str=" + "):
        # Join the gem names, if they are in the selected skill group and if they are enable d. Show quality and level
        # if level is >20 or quality is set.
        ret = join_str.join([gem.build_gem_string() for gem in self.gems if gem.is_valid_gem()])

        if item:
            supports = item.added_supports
            if supports and isinstance(supports, list):
                ret += "\n(+ " + join_str.join([gem['name'] + " (" + gem['level'] + ")" for gem in supports])
                ret += f" from: *{item.name}*)"
        return ret
