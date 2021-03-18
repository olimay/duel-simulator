# player.py

from cards import *
from weaponsarmor import *

def make_player(name, hp = 100, max_hp = 100, inventory = None) -> dict:
  player = {}
  player['name'] = name
  player['weapon'] = None
  player['armor'] = None
  player['cards'] = make_hand()
  player['hp'] = hp
  player['max_hp'] = max_hp
  if inventory is None:
    player['inventory'] = make_player_inventory()
  else:
    player['inventory'] = copy_player_inventory(inventory)
  return player

def player_copy(p) -> dict:
  c = {}
  c['name'] = p['name']
  c['weapon'] = p['weapon']
  c['armor'] = p['armor']
  c['cards'] = hand_copy(p['cards'])
  c['hp'] = p['hp']
  c['max_hp'] = p['max_hp']
  c['inventory'] = copy_player_inventory(p['inventory'])
  return c

def make_player_inventory() -> dict:
  i = {}
  i['weapons'] = []
  i['armor'] = []
  i['special'] = {}
  return i

def copy_player_inventory(i) -> dict:
  c = {
      'weapons' : [w.copy() for w in i['weapons']],
      'armor' : [a.copy() for a in i['armor']],
      'special' : i['special'].copy() # this is just a dict
  }
  return c

def inventory_add_item(i, name : str, count = 1):
  special = i['special']
  if name in special.keys():
    special[name] += count
  else:
    special[name] = count

def inventory_remove_item(i, name : str, count = 1):
  special = i['special']
  if name in special.keys():
    special[name] -= count
    if special[name] <= 0:
      removed_item = special.pop(name)
  else:
    print("Warning: item {} not found inventory.".format(name))

def inventory_count_item(i, name : str) -> int:
  special = i['special']
  if name in special.keys():
    return special[name]
  return 0

def inventory_has_weapon(i, w):
  for W in i['weapons']:
    if W['name'] == w['name']:
      return True
  return False

def inventory_has_armor(i, a):
  for A in i['weapons']:
    if A['name'] == a['name']:
      return True
  return False

def inventory_add_weapon(i, w):
  if not inventory_has_weapon(i, w):
    i['weapons'] += [clone_equipment(w)]
  else:
    print("Warning: already have a weapon {} in inventory".format(w['name']))

def inventory_add_armor(i, a):
  if not inventory_has_armor(i, a):
    i['armor'] += [clone_equipment(a)]
  else:
    print("Warning: already have an armor {} in inventory".format(a['name']))

def inventory_replace_weapon(i, w_i, w):
  weapons = i['weapons']
  if w is None: # if none, interpret as deletion
    weapons.pop(w_i)
  else:
    weapons[w_i] = clone_equipment(w)

def inventory_replace_armor(i, a_i, a):
  armor = i['armor']
  if a is None: # if none, interpret as deletion
    armor.pop(a_i)
  else:
    armor[a_i] = clone_equipment(a)

def inventory_weapon_count(i):
  return len(i['weapons'])

def inventory_armor_count(i):
  return len(i['armor'])

def inventory_get_weapon_name(i, w_i):
  weapons = i['weapons']
  if w_i < inventory_weapon_count(i):
    return weapons[w_i]['name']
  return None

def inventory_get_armor_name(i, a_i):
  armor = i['armor']
  if a_i < inventory_armor_count(i):
    return armor[a_i]['name']
  return None

def equip_weapon(player, weapon) -> dict:
  p = player
  p['weapon'] = weapon

def equip_armor(player, armor) -> dict:
  p = player
  p['armor'] = armor

def requip_weapon(plr, w_i):
  inv = plr['inventory']
  inv_w = inv['weapons']
  if w_i >= 0 and w_i < inventory_weapon_count(inv):
    equip_weapon(plr, inv_w[w_i])
  else:
    raise Exception(
        "Invalid weapon index {} (out of {})".format(
          w_i,
          inventory_weapon_count(inv)
          ))

def requip_armor(plr, a_i):
  inv = plr['inventory']
  inv_a = inv['armor']
  if a_i >= 0 and a_i < inventory_armor_count(inv):
    equip_armor(plr,inv_a[a_i])
  else:
    raise Exception(
        "Invalid armor index {} (out of {})".format(
          a_i,
          inventory_armor_count(inv)
          ))

def test_make_player():
  plr_A = make_player("Cloud Strife")
  plr_B = make_player("Carmine Ragussa")
  return plr_A, plr_B

def test_player_draw_hand():
  A, B = test_make_player()
  deck = make_deck()
  A['cards'], deck = draw_hands(A['cards'], deck)
  return A

def test_equip():
  A, B = test_make_player()
  equip_weapon(A, buster_sword) 
  equip_armor(A, plate_mail)
  equip_weapon(B, rapier)
  equip_armor(B, leather)

def test_make_player_inventory():
  ex_inventory = make_player_inventory()
  juan = make_player("Juan Santana")
  assert len(juan['inventory']) == len(ex_inventory) 
  assert type(juan['inventory']) == dict
  print("OK")

def test_inventory_add_item():
  juan = make_player("Juan Santana")
  inv = juan['inventory']
  inv_spe = inv['special']
  for x in range(10):
    inventory_add_item(inv, "cheese", 10)
  assert len(inv_spe) == 1
  assert inventory_count_item(inv, "cheese") == 10*10
  assert inventory_count_item(inv, "rock salt") == 0
  assert inventory_count_item(inv, "cheese") == 10*10
  assert inventory_count_item(inv, "rock salt") == 0
  inventory_remove_item(inv, "rock salt", 200)
  inventory_remove_item(inv, "cheese", 50)
  assert len(inv_spe) == 1
  assert inventory_count_item(inv, "cheese") == 10*10-50
  inventory_remove_item(inv, "cheese", 49)
  inventory_remove_item(inv,"cheese", 1)
  assert len(inv_spe) == 0, "Expected 0, got {}".format(len(inv_spe))
  print("OK!")

def test_add_remove_weapon():
  juan = make_player("Juan Santana")
  inv = juan['inventory']
  inv_s = inv['special']
  inv_w = inv['weapons']
  inv_a = inv['armor']
 
  assert len(inv_s) == 0, "Expected 0, got {}".format(len(inv_s))
  assert len(inv_w) == 0, "Expected 0, got {}".format(len(inv_w))
  assert len(inv_a) == 0, "Expected 0, got {}".format(len(inv_a))
  assert inventory_has_weapon(inv, rapier) == False

  inventory_add_weapon(inv, rapier)
  assert inventory_has_weapon(inv, rapier) == True
  assert inventory_weapon_count(inv) == 1
  assert inventory_get_weapon_name(inv, 0) == rapier['name'], (
      "Got {}, Expected {}".format(inventory_get_weapon_name(inv,0),rapier['name'])
      )
  
  inventory_add_weapon(inv, rapier)
  inventory_add_weapon(inv, rapier)
  assert inventory_has_weapon(inv, rapier) == True
  assert inventory_weapon_count(inv) == 1
  assert inventory_get_weapon_name(inv, 1) is None

  inventory_replace_weapon(inv, 0, buster_sword)
  assert inventory_has_weapon(inv, rapier) == False
  assert inventory_has_weapon(inv, buster_sword) == True
  assert inventory_weapon_count(inv) == 1
  assert inventory_get_weapon_name(inv, 0) == buster_sword['name']

  inventory_replace_weapon(inv, 0, None)
  assert inventory_has_weapon(inv, rapier) == False
  assert inventory_has_weapon(inv, buster_sword) == False
  assert inventory_weapon_count(inv) == 0
  assert inventory_get_weapon_name(inv, 0) is None

  print("OK!")

def test_requip():
  juan = make_player("Juan Santana")
  inv = juan['inventory']
  inventory_add_weapon(inv, rapier)
  inventory_add_weapon(inv, buster_sword)
  inventory_add_armor(inv, plate_mail)
  inventory_add_armor(inv, leather) 
  jw = juan['weapon']
  ja = juan['armor']
  assert jw is None
  assert ja is None
  requip_weapon(juan, 0)
  requip_armor(juan, 1)
  jw = juan['weapon']
  ja = juan['armor']
  assert jw['name'] == rapier['name']
  assert ja['name'] == leather['name']
  requip_weapon(juan, 1)
  requip_armor(juan, 0)
  jw = juan['weapon']
  ja = juan['armor']
  assert jw['name'] == buster_sword['name']
  assert ja['name'] == plate_mail['name']
  print("OK!")

