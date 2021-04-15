class Gem:
    __slots__ = 'name', 'level', 'quality', 'id', 'skill_part', 'enabled', 'second_name', 'active_part', 'is_active', \
                'selected_minion', 'minion_skill', 'quality_type', 'base_name', 'instance_count'

    def __init__(self, gem_id, name, level, quality, skill_part, enabled='', instance_count=1, selected_minion=None,
                 minion_skill=False,
                 quality_id='Default'):
        self.level = int(level)
        self.quality = int(quality)
        self.id = gem_id
        self.skill_part = int(skill_part) if skill_part else None
        self.enabled = True if enabled == 'true' else False
        self.second_name = name.split("Vaal ", 1)
        if len(self.second_name) > 1:
            self.second_name = self.second_name[1]
        else:
            self.second_name = None
        self.active_part = 0
        self.selected_minion = selected_minion
        self.minion_skill = minion_skill
        self.is_active = self.determine_active()
        self.quality_type = self.translate_pob_quality_id(quality_id)
        self.base_name = self.translate_name(gem_id) if name == "" else name
        full_name = ''
        if self.quality_type:
            full_name += f"{self.quality_type} "
        full_name += self.base_name
        self.name = full_name
        try:
            self.instance_count = int(instance_count) if instance_count else 1
        except ValueError:
            self.instance_count = 1

    def __repr__(self) -> str:
        return f"Gem [{self.build_gem_string()}]"

    def determine_active(self):
        return False if not self.id else "Support".lower() not in self.id.lower()

    def get_name(self):
        return self.name if self.active_part == 0 else self.second_name

    def set_active_part(self, part_id):
        self.active_part = part_id

    def build_gem_string(self):
        """
        Get the display string for a gem, adds level and quality info if the gem is remarkable in some way.
        :return: information string: name | name (level/quality)
        """
        exceptional_gems = ['empower', 'enlighten', 'enhance']
        gem_string = self.name

        special_gem = self.name.lower() in exceptional_gems
        high_level = self.level > 20
        is_notable = self.quality > 5

        if special_gem or high_level or is_notable:
            gem_string += f" ({self.level}/{self.quality}%)"
        return gem_string

    def is_valid_gem(self):
        """
        A gem is valid if it's enabled, it has a nonempty, non jewel name
        :return: true if it is a parseable gem
        """
        return self.name and self.enabled and self.name != '' and 'jewel' not in self.name.lower()

    @staticmethod
    def translate_name(skill_id):
        special_names = {
            'UniqueAnimateWeapon': 'Manifest Dancing Dervish',
            'ChaosDegenAuraUnique': "Death Aura",
            'IcestormUniqueStaff12': "Ice Storm",
            'TriggeredMoltenStrike': "Molten Burst",
            'TriggeredSummonSpider': "Raise Spiders",
            'AvianTornado': "Tornado"
        }
        return special_names.get(skill_id, '')

    @staticmethod
    def translate_pob_quality_id(qualityId: str):
        alternate_quality_ids = {
            'Alternate1': 'Anomalous',
            'Alternate2': 'Divergent',
            'Alternate3': 'Phantasmal',
        }
        return alternate_quality_ids.get(qualityId, None)
