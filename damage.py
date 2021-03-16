# guidelines:
# trying to go for the following:
# 1. two consecutive successful attacks at full strength with the other player
#    missing should win
# 2. typical duel length should be 5-6 rounds
# 3. if evenly matched with no particular strategy, each player wins about 35%
#     of the time, and end up in a draw about 30% of the time
# the following suggests that a "big" attack be ~60 and the base attack be ~30
"""
>>> randomwalk.simulate(60,30,1000000)
range = [2,113]
greater than 10: 0.307808
mean = 9.190085
"""

import math

# here are some defaults that can be overwritten

# stack constant values (positive numbers, default to 0)
# ===
BASE_OFFSET = 10
BASE_ATTACK_FACTOR = 1.2
MAX_BASE_STACK = 20
# should be an integer in [0,10] independent of MAX_BASE_STACK
EFFECTIVE_BASE_STACK = 0 
# added separately, so should be based on MAX_BASE_STACK
WEAPONTYPE_STACK = 0
WEAPON_STRAIGHT_STACK = WEAPONTYPE_STACK * 0.25
WEAPONCLASS_STACK = {
      'C': MAX_BASE_STACK * 0.0,
      'B': MAX_BASE_STACK * 0.1,
      'A': MAX_BASE_STACK * 0.2,
      'S': MAX_BASE_STACK * 0.3,
    }
ARMORTYPE_STACK = MAX_BASE_STACK * 0.1 
ARMOR_GUARD_STACK = ARMORTYPE_STACK * 0.5
ARMORCLASS_STACK = {
      'C': MAX_BASE_STACK * 0.05,
      'B': MAX_BASE_STACK * 0.10,
      'A': MAX_BASE_STACK * 0.15,
      'S': MAX_BASE_STACK * 0.20,
    }

# mult constant values (should default to 1)
# ===
BASE_EFFECTIVE_MULT = 1.25
WEAPONTYPE_MULT = 1.5
WEAPON_STRAIGHT_MULT = 1
WEAPONCLASS_MULT = {
      'C': 1,
      'B': 1,
      'A': 1,
      'S': 1,
    }
ARMORTYPE_MULT = 1
ARMOR_GUARD_MULT = 1
ARMORCLASS_MULT = {
      'C': 1,
      'B': 1,
      'A': 1,
      'S': 1,
    }

# validation functions: return true or raise exceptions

def valid_attack(attack_type):
  if not (attack_type in ['S','T','L']):
    raise Exception("Invalid attack {}".format(attack_type))
  return True

def valid_defense(defense_type):
  if not (defense_type in ['D', 'P', 'B']):
    raise Exception("Invalid defense {}".format(defense_type))
  return True

def valid_weapontype(weapon_type):
  if not weapon_type in ['H', 'F', 'K', 'S']:
    raise Exception("Invalid weapon type {}".format(weapon_type))
  return True

def valid_armortype(armor_type):
  if not armor_type in ['D', 'B', 'P', 'G']:
    raise Exception("Invalid armor type {}".format(armor_type))
  return True

def valid_equipmentclass(equip_class):
  if not equip_class in ['C', 'B', 'A', 'S']:
    raise Exception("Invalid equipment class {}".format(equip_class))
  return True


def valid_attack(attack_type):
  if not attack_type in ['S', 'T', 'L']:
    raise Exception("Invalid attack type {}".format(attack_type))
  return True

def valid_defense(defense_type):
  if not defense_type in ['D', 'P', 'B']:
    raise Exception("Invalid defense type {}".format(defense_type))
  return True

# stack bonuses/penalties
def stack_base(attack_type, defense_type, attack_strength, defense_strength) -> int:
  if valid_attack(attack_type) and valid_defense(defense_type):
    pass
  # effectiveness of attack is not handled here
  # effective = { 'S' : 'P', 'T' : 'B', 'L' : 'D', }
  # maximum base damage for an effective attack: (10 - 1)*
  effective = { 'S' : 'P', 'T' : 'B', 'L' : 'D', }
  effective_bonus = EFFECTIVE_BASE_STACK if effective[attack_type] == defense_type else 0
  return (attack_strength*BASE_ATTACK_FACTOR - defense_strength + BASE_OFFSET + effective_bonus)/10*MAX_BASE_STACK

def stack_weapontype(weapon_type, attack_type) -> int:
  if valid_weapontype(weapon_type) and valid_attack(attack_type):
    pass
  if weapon_type == 'S':
    return WEAPON_STRAIGHT_STACK
  specialty = {
      'F' : 'T',
      'H' : 'S',
      'K' : 'L',
      'S' : 'Q', # just need the key to be in the dict
      }
  return WEAPONTYPE_STACK if specialty[weapon_type] == attack_type else 0

def stack_weaponclass(weapon_class) -> int:
  if valid_equipmentclass(weapon_class):
    pass
  return WEAPONCLASS_STACK[weapon_class]

def stack_armortype(armor_type, defense_type) -> int:
  if valid_armortype(armor_type) and valid_defense(defense_type):
    pass
  if armor_type == 'G':
    return ARMOR_GUARD_STACK
  return ARMORTYPE_STACK if armor_type == defense_type else 0

def stack_armorclass(armor_class) -> int:
  if valid_equipmentclass(armor_class):
    pass
  return ARMORCLASS_STACK[armor_class]

# multiplier bonuses/penalties
def mult_negate(attack_type, defense_type) -> float:
  if valid_attack(attack_type) and valid_defense(defense_type):
    pass
  negates = {
    'S' : 'D',
    'T' : 'P',
    'L' : 'B',
    }
  return 0 if negates[attack_type] == defense_type else 1

def mult_base(attack_type, defense_type, attack_strength, defense_strength) -> float:
  if valid_attack(attack_type) and valid_defense(defense_type):
    pass
  effective = { 'S' : 'P', 'T' : 'B', 'L' : 'D', }
  return BASE_EFFECTIVE_MULT if effective[attack_type] == defense_type else 1

def mult_weapontype(weapon_type, attack_type) -> float:
  if valid_weapontype(weapon_type) and valid_attack(attack_type):
    pass
  if weapon_type == 'S':
    return WEAPON_STRAIGHT_MULT
  specialty = {
      'F' : 'T',
      'H' : 'S',
      'K' : 'L',
      }
  return WEAPONTYPE_MULT if specialty[weapon_type] == attack_type else 1

def mult_weaponclass(weapon_class) -> float:
  if valid_equipmentclass(weapon_class):
    pass
  return WEAPONCLASS_MULT[weapon_class]

def mult_armortype(armor_type, defense_type) -> float:
  if valid_armortype(armor_type) and valid_defense(defense_type):
    pass
  return ARMORTYPE_MULT if armor_type == defense_type else 1

def mult_armorclass(armor_class) -> float:
  if valid_equipmentclass(armor_class):
    pass
  return ARMORCLASS_MULT[armor_class]

def damage(attack_type : str, defense_type : str, attack_strength : int,
    defense_strength : int, weapon_type : str, weapon_class : str,
    armor_type : str, armor_class : str, event = None) -> int:
  # default values if there is no event function passed in
  stack_event = 0
  mult_event = 1
  if not (event is None) and callable(event):
    stack_event, mult_event = event(
        attack_type,
        defense_type,
        attack_strength,
        defense_strength,
        weapon_type,
        weapon_class,
        armor_type,
        armor_class
        )
  # damage =[ stuff to add ] * [ stuff to multiply ] - a hit will always cause 1 damage
  dmg = max(
     math.floor(
       (stack_base(attack_type, defense_type,
       attack_strength, defense_strength) +
       stack_weapontype(weapon_type, attack_type) +
       stack_weaponclass(weapon_class) -
       stack_armortype(armor_type, defense_type) -
       stack_armorclass(armor_class)
       ) * 
       (mult_base(attack_type, defense_type,
         attack_strength, defense_strength) *
         mult_weapontype(weapon_type, attack_type) *
         mult_weaponclass(weapon_class) *
         mult_armortype(armor_type, defense_type) *
         mult_armorclass(armor_class)
         )
     ),1)
  assert dmg >= 1, "calculated damage before counter {} < 1".format(dmg)
  return mult_negate(attack_type, defense_type) * dmg
