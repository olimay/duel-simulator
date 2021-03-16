# player.py

from cards import *

def make_player(name, hp = 100, max_hp = 100) -> dict:
  player = {}
  player['name'] = name
  player['weapon'] = None
  player['armor'] = None
  player['cards'] = make_hand()
  player['hp'] = hp
  player['max_hp'] = max_hp
  return player

def player_copy(p) -> dict:
  c = {}
  c['name'] = p['name']
  c['weapon'] = p['weapon']
  c['armor'] = p['armor']
  c['cards'] = hand_copy(p['cards'])
  c['hp'] = p['hp']
  c['max_hp'] = p['max_hp']
  return c

def equip_weapon(player, weapon) -> dict:
  p = player
  p['weapon'] = weapon

def equip_armor(player, armor) -> dict:
  p = player
  p['armor'] = armor

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


