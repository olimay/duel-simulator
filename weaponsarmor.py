# weapons-armor.py
# weapons and armor

WEAPON_TYPES = ['F', 'K', 'H', 'S']
WEAPON_ARMOR_STRENGTHS = ['C','B','A','S']

def make_weapon(name, weapon_type, strength, description = "", details = None,
        special = None) -> dict:
    weapon = {}
    if not weapon_type in WEAPON_TYPES:
        raise(Exception("Invalid weapon type: {}".format(weapon_type)))
    if not strength in WEAPON_ARMOR_STRENGTHS:
        raise(Exception("Invalid weapon strength: {}".format(strength)))
    weapon['name'] = name
    weapon['type'] = weapon_type
    weapon['strength'] = strength
    weapon['description'] = description
    weapon['details'] = details
    if type(special) == list:
        weapon['special'] = special
    elif type(special) == dict:
        weapon['special'] = [special]
    elif special is None:
        weapon['special'] = []
    else:
        msg = "type(special)={}; expected list, dict, or None"
        raise Exception(msg.format(type(special)))
    return weapon


ARMOR_TYPES = ['D', 'B', 'P', 'G']
# D: enhanced dodge
# B: enhanced block
# P: enhanced parry
# G: partial all around boost

def make_armor(name, armor_type, strength, description = "", details = None,
        special = None) -> dict:
    armor = {}
    if not armor_type in ARMOR_TYPES:
        raise(Exception("Invalid armor type: {}".format(armor_type)))
    if not strength in WEAPON_ARMOR_STRENGTHS:
        raise(Exception("Invalid armor strength: {}".format(strength)))
    armor['name'] = name
    armor['type'] = armor_type
    armor['strength'] = strength
    armor['description'] = description
    armor['details'] = details
    if type(special) == list:
        armor['special'] = special
    elif type(special) == dict:
        armor['special'] = [special]
    elif special is None:
        armor['special'] = []
    else:
        msg = "type(special)={}; expected list, dict, or None"
        raise Exception(msg.format(type(special)))
    return armor

def clone_equipment(eq):
    if eq['type'] in ARMOR_TYPES:
        return make_armor(eq['name'], eq['type'], eq['strength'],
                eq['description'], eq['details'],
                [s.copy() for s in eq['special']])
    if eq['type'] in WEAPON_TYPES:
        return make_weapon(eq['name'], eq['type'], eq['strength'],
                eq['description'], eq['details'],
                [s.copy() for s in eq['special']])

def print_equipment(equipment : dict):
    equipment_type = "Weapon" if equipment['type'] in WEAPON_TYPES else "Armor"
    print("###\n{} : {}".format(equipment_type, equipment['name']))
    print("{} Type {} Class {}".format(
        equipment_type,
        equipment['type'],
        equipment['strength'],
        )
        )
    print("Description: {}".format(equipment['description']))
    print("Details: {}".format(equipment['details']))

buster_sword = make_weapon("Buster Sword", "H", "A", "A large broadsword that has inherited the hopes of those who fight.")
rapier = make_weapon("Rapier", "F", "C", "Better than an epee.")
zxv_sword = make_weapon("The ZXV Sword", "S", "S", "The best.")
plate_mail = make_armor("Plate Mail", "B", "A", "Very strong lol")
fencing_gear = make_armor("Fencing Gear", "P", "B", "Keeps you agile")
chocobo_suit = make_armor("Chocobo Suit", "D", "S", "Waark")
leather = make_armor('Leather Bracers','P','C',"Leather armor yo")

def test_make_weapon():
    print_equipment(buster_sword)
    print_equipment(rapier)
    print_equipment(zxv_sword)

def test_make_armor():
    print_equipment(plate_mail)
    print_equipment(fencing_gear)
    print_equipment(chocobo_suit)
    print_equipment(leather)

def test_weapon_armor():
    test_make_weapon()
    test_make_armor()

def test_clone_equipment():
    fapier = clone_equipment(rapier)
    fapier['name'] = "Fapier"
    fapier['strength'] = "F"
    fapier['description'] = 'A floppy sword entrusted with the hope of those who fap'
    print_equipment(rapier)
    print_equipment(fapier)
    flate_mail = clone_equipment(plate_mail)
    flate_mail['name'] = "Flate Mail" 
    flate_mail['strength'] = "F" 
    flate_mail['description'] = 'Looks like plate mail, but is just made of balloons'
    print_equipment(plate_mail)
    print_equipment(flate_mail)
    print("OK!")
