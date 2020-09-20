import re

from poediscordbot.util.logging import log


class ItemSlot:
    __slots__ = 'active', 'item', 'item_id', 'name'

    def __init__(self, name, item_id, item, active=False):
        self.name = name
        self.item_id = item_id
        self.item = item
        self.active = bool(active)

    def __repr__(self) -> str:
        return f"ItemSlot [name={self.name}; item_id={self.item_id}; item={self.item}; active={self.active}]"


class Item:
    __slots__ = 'id', 'raw_content', 'variant', 'name', 'added_supports'

    def __init__(self, item_id, raw_content, variant=None):
        self.id = item_id
        self.raw_content = raw_content.strip()
        self.variant = variant
        self.name = self.parse_item_name()
        self.added_supports = self.parse_item_for_support()

    def __repr__(self) -> str:
        return f"Item [id={self.id}; name={self.name}; Supports={self.added_supports}]"

    def parse_item_name(self):
        # see here for regex: https://regex101.com/r/MivGPM/1
        regex = r"\s*Rarity:.*\n\s*(.*)\n"
        matches = re.findall(regex, self.raw_content, re.IGNORECASE)
        try:
            name = matches[0]
        except IndexError as err:
            log.warning(f"Item parsing: Name could not be retrieved. Trying string split method Err={err}")
            name = self.raw_content.split('\n')[0]

        return name

    def parse_item_for_support(self):
        # Socketed Gems are Supported by level 20 Elemental Proliferation
        add_supports = []
        # see here for regex: https://regex101.com/r/CcxRuz/1
        pattern = r"({variant:([0-9,]*)}|)Socketed Gems are Supported by level ([0-9]*) ([a-zA-Z ]*)"
        try:
            supports = re.findall(pattern, self.raw_content, re.IGNORECASE)
            for support in supports:
                # if either no variant exists, or our variant matches the current supports variant
                if 'variant' not in support[0] or self.variant in support[0]:
                    add_supports.append({"name": support[3], "level": support[2]})
        except AttributeError as err:
            return
        return add_supports
