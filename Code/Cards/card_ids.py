"""
Card ID System:
- First 3 digits = card type (000=Offense, 001=Defense, 002=Utility)
- Remaining digits = unique card number within that type
- Examples:
  - 0001 = Offense card #1
  - 0009483721 = Offense card #9483721
  - 1001 = Defense card #1
  - 2001 = Utility card #1
"""

# Type codes
OFFENSE_TYPE = 0
DEFENSE_TYPE = 1
UTILITY_TYPE = 2


def get_card_type(card_id: int) -> int:

    stringed_id = str(card_id).zfill(4)  # Ensure at least 4 digits (3 for type + 1 for card)
    type_code = stringed_id[0:3]
    return int(type_code)


def get_card_number(card_id: int) -> int:
    stringed_id = str(card_id).zfill(4)
    card_num = stringed_id[3:]
    return int(card_num)


# === OFFENSE CARDS (have images) ===
STRIKE = 1  # Will be interpreted as 0001
SLASH = 2
HEAVY_STRIKE = 3

# === OFFENSE CARDS (no unique images - commented out) ===
# EXECUTE = 4
# POISON_STRIKE = 5
# AREA_ATTACK = 6

# === DEFENSE CARDS (have images) ===
SHIELD_UP = 1001
DODGE = 1002
REGENERATION = 1005
HEAL = 1006

# === DEFENSE CARDS (no unique images - commented out) ===
# ARMOR_UP = 1003
# COUNTER_ATTACK = 1004
# PARRY = 1007

# === UTILITY CARDS (no unique images - all commented out) ===
# DRAW_CARDS = 2001
# DRAW_AND_DISCOUNT = 2002
# BATTLE_RAGE = 2003
# MANA_GAIN = 2004
# DISCARD_FOR_POWER = 2005
# CYCLE = 2006
# DUPLICATE = 2007
# UPGRADE_CARD = 2008
# COST_REDUCTION = 2009
# EXHAUST_FOR_EFFECT = 2010
# SCRY = 2011