from enum import Enum


class OutputThresholds(Enum):
    # Basic Defense
    LIFE_FLAT_THRESHOLD = 1000
    LIFE_REGEN_THRESHOLD = 100
    ES_THRESHOLD = 300
    ES_REGEN_THRESHOLD = 100
    MAX_RES_THRESHOLD = 75

    ARMOUR_THRESHOLD = 5000
    EVASION_THRESHOLD = 5000

    # most shields have 25-30 base, so +10 should be easily doable, spellblock is lower
    BLOCK_THRESHOLD = 40
    SPELLBLOCK_THRESHOLD = 20
    # 30 = Acro/Phase Acro
    DODGE_THRESHOLD = 30
    SPELLDODGE_THRESHOLD = 30