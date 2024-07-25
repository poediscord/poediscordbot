from instance import config

from poediscordbot.cogs.pob.output.aggregators.abstract_aggregator import AbstractAggregator
from poediscordbot.util.logging import log


class ConfigAggregator(AbstractAggregator):
    minified = False

    def get_output(self) -> (str, str):
        return 'Configuration', self.get_config_string(self.build.config,
                                                       self.build.skills)

    @staticmethod
    def special_ignored_case(name, value):
        if name == 'Exposure to' and value == '0':
            return True
        return False

    @staticmethod
    def prepare_config_line(name, value):
        """
        Create the entry for one specific configuration with it's name and value
        :param name:
        :param value:
        :return: string
        """
        conf_item = f'{name}'
        if not ConfigAggregator.special_ignored_case(name, value):
            if value and value.lower() != 'true':
                conf_item += f': {value.capitalize()}'
            return conf_item

    @staticmethod
    def has_gem_precondition(skills, if_skill_list):
        """
        Check if we have any skill active preconditions and try to
        match at least one of active gems with it
        :param skills: list of skills from a Build object
        :param if_skill_list: list of skill preconditions from config
        :return: true if precondition is met, false otherwise
        """
        for skill in skills:
            if not skill.enabled:
                continue

            for gem in skill.gems:
                if not gem.enabled:
                    continue

                if gem.get_name() in if_skill_list:
                    return True

        return False

    @staticmethod
    def get_config_string(build_conf, skills):
        """
        Use the given config to extract one string for the output.
        :param build_conf: a dictionary of configs from a Build object
        :param skills: list of skills from a Build object
        :return: string representation
        """
        configs = {}
        for key, entry in build_conf.items():
            abbrev = entry.get('abbreviation')
            value = entry.get('value')
            category = entry.get('category')
            ifOption = entry.get('ifOption')

            # Skip conditional options that are not matching precondition in output
            if ifOption and (ifOption not in build_conf or not
            bool(build_conf.get(ifOption).get('value'))):
                continue

            if_skill = entry.get('ifSkill')
            if_skill_list = entry.get('ifSkillList', [])
            if if_skill:
                if_skill_list.append(if_skill)

            if value and value.lower() != 'false':
                config_line = ConfigAggregator.prepare_config_line(abbrev if abbrev else key, value)
                if category and config_line:
                    if if_skill_list and not ConfigAggregator.has_gem_precondition(skills, if_skill_list):
                        continue

                    configs.setdefault(category.capitalize(), []).append(config_line)
                elif key == 'customMods':
                    continue
                else:
                    log.warn(
                        f"Category='{category}' or config_line='{config_line}' not set or unknown, check 'pob_conf.json'"
                        f"for entries with mixing categories and abbreviations. "
                        f"This happens after pob introduces new values. If one of the values is `None` you need to "
                        f"update the json file similarly to the existing entries.")
        out = ''
        for category in configs:
            if len(configs[category]) > 0:
                out += '**' + category + '**: '
                out += ', '.join(configs[category])
                out += '\n'

        #handle custom config and line cutting
        custom_mods = build_conf.get('customMods')
        if build_conf and custom_mods:
            custom_lines = custom_mods.get('value').split("\n")
            custom_text = ""
            custom_line_max = 5 if config.custom_mods_lines is None else config.custom_mods_lines

            if custom_line_max > 0:
                if len(custom_lines) > custom_line_max:
                    custom_text += f"only showing the first {custom_line_max} of {len(custom_lines)} lines"
                for line in custom_lines[:custom_line_max]:
                    custom_text += f"\n-# {line}"

                out += f'**Custom**: {custom_text}'
        return out if out != '' else None
