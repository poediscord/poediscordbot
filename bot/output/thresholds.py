from enum import Enum


class OutputThresholds(Enum):
    # Basic Defense
    LIFE_FLAT = 1000
    LIFE_PERCENT = 50
    LIFE_REGEN = 100

    ES_FLAT = 300
    ES_PERCENT = 50
    ES_REGEN = 100

    MAX_RES = 75

    ARMOUR = 3000
    EVASION = 3000

    # most shields have 25-30 base, so +10 should be easily doable, spellblock is lower
    BLOCK = 40
    SPELL_BLOCK = 20
    # 30 = Acro/Phase Acro
    DODGE = 30
    SPELL_DODGE = 30

    #Offense
    ACCURACY = 95
    CRIT_CHANCE = 5