import math

# stack constant values (positive numbers, default to 0)
# ===
BASE_OFFSET = 10
BASE_ATTACK_FACTOR = 1.2
MAX_BASE_STACK = 35
# should be an integer in [0,10] independent of MAX_BASE_STACK
EFFECTIVE_BASE_STACK = 0 
# added separately, so should be based on MAX_BASE_STACK
WEAPONTYPE_STACK = 0
WEAPON_STRAIGHT_STACK = WEAPONTYPE_STACK * 0.25
WEAPONCLASS_STACK = {
      'C': MAX_BASE_STACK * 0.0,
      'B': MAX_BASE_STACK * 0.12,
      'A': MAX_BASE_STACK * 0.24,
      'S': MAX_BASE_STACK * 0.36,
    }
ARMORTYPE_STACK = MAX_BASE_STACK * 0.1 
ARMOR_GUARD_STACK = ARMORTYPE_STACK * 0.5
ARMORCLASS_STACK = {
      'C': MAX_BASE_STACK * 0.00,
      'B': MAX_BASE_STACK * 0.06,
      'A': MAX_BASE_STACK * 0.12,
      'S': MAX_BASE_STACK * 0.18,
    }

# mult constant values (should default to 1)
# ===
BASE_EFFECTIVE_MULT = 1.25
WEAPONTYPE_MULT = 1.25
WEAPON_STRAIGHT_MULT = 1.075
WEAPONCLASS_MULT = {
      'C': 1,
      'B': 1,
      'A': 1,
      'S': 1,
    }
ARMORTYPE_MULT = 1/1.3
ARMOR_GUARD_MULT = 1/1.05
ARMORCLASS_MULT = {
      'C': 1/1,
      'B': 1/1.05,
      'A': 1/1.1,
      'S': 1/1.15,
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
     math.ceil(
       (stack_base(attack_type, defense_type,
       attack_strength,defense_strength) +
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

def test_damage():
  a_types = ['S', 'T', 'L']
  d_types = ['D', 'P', 'B']
  wp_types = ['H', 'F', 'K', 'S']
  ar_types = ['D', 'B', 'P', 'G']
  ratings = ['C', 'B', 'A', 'S']
  for wp in wp_types:
    for wr in ratings:
      print("Weapon {} {}".format(wp, wr))
      for ar in ar_types:
        for arr in ratings:
          print("Armor Type: {}".format(ar, arr))
          for a in a_types:
            for d in d_types:
              for a_s in range(1,10):
                for d_s in range(1,10):
                  dmg = damage(a, d, a_s, d_s, wp, wr, ar, arr)
                  msg = "{}{} vs {}{} : {} damage".format(
                      a,
                      a_s,
                      d,
                      d_s,
                      dmg
                      )
                  print(msg)

