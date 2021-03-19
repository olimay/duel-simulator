# demo runner

from duel import *
from weaponsarmor import *
import math
import os

jor_feig = make_armor(
    "JorFeig Everyday Casual",
    "G",
    "C",
    description = "Comfortable casual wear with stylish NUANCE.",
    details = None,
    special = None
    )
fencing_sword = make_weapon(
    "Fencing Sword",
    "F",
    "C",
    description = "Your trusty fencing foil, good for thrusting.",
    details = None,
    special = None
    )
fencing_gear = make_armor(
    "Fencing Gear",
    "P",
    "B",
    description = "",
    details = None,
    special = None
    )
buster_barbell = make_weapon(
    "Buster Barbell",
    "H",
    "B",
    description = "A large steel barbell that has inherited the hopes of those who lift.",
    details = None,
    special = None
    )
mukbang_magus_robe = make_armor(
    "Mukbang Magus Robe",
    "B",
    "A",
    description = "",
    details = None,
    special = None
    )
curved_wooden_spoon = make_weapon(
    "Curved Wooden Spoon",
    "K",
    "A",
    description = "",
    details = None,
    special = None
    )
waaarkout_clothes = make_armor(
    "Waaarkout Clothes",
    "D",
    "S",
    description = "",
    details = None,
    special = None
    )
zxv_sword = make_weapon(
    "The ZXV Sword",
    "S",
    "S",
    description = "ZXV SWORD",
    details = None,
    special = None
    )
sealed_weapon = make_weapon(
    "Sealed Weapon",
    "K",
    "C",
    description = "No. NooooOOOO. This weapon is wrapped in something suspicious.",
    details = None,
    special = None
    )

#
def keyboard_warrior():
  p = make_player("The Keyboard Warrior")
  w = make_weapon(
      "Flamewar Rapier",
      "F",
      "B",
      description = "",
      details = None,
      special = None
      )
  a = make_armor(
      "Brigandine of Bad Faith",
      "B",
      "C",
      description = "",
      details = None,
      special = None
      )
  equip_weapon(p, w)
  equip_armor(p, a)
  return p

def stalker():
  p = make_player("Stalker")
  w = make_weapon(
      "Stalker Shamshir",
      "K",
      "A",
      description = "",
      details = None,
      special = None
      )
  a = make_armor(
      "Creeper Robes",
      "D",
      "B",
      description = "",
      details = None,
      special = None
      )
  equip_weapon(p, w)
  equip_armor(p, a)
  return p


def computer_bug():
  p = make_player("Computer Bug")
  w = make_weapon(
      "Greataxe of BSOD",
      "H",
      "S",
      description = "",
      details = None,
      special = None
      )
  a = make_armor(
      "Glitch Shroud",
      "G",
      "A",
      description = "",
      details = None,
      special = None
      )
  equip_weapon(p, w)
  equip_armor(p, a)
  return p


def hp_bar(hp1, hp2, p1ch = "*", p2ch = "o", sep = "|", col = 60):
  total = hp1 + hp2 
  bar_col = col - 3
  template = "[{}{}{}]"
  cols1 = math.floor(hp1/total * bar_col)
  cols2 = math.ceil(hp2/total * bar_col)
  return (template.format(p1ch * cols1, sep, p2ch * cols2))


def test_hp_bar(col = 60):
  X = [h for h in range(200, 0, -13)]
  for x in X:
    print(hp_bar(x, 200-x, col = col) + " {} ".format(x))

def right_just(s, col = 60, c = " "):
  return c*(col - len(s)) + s

def equip_type_str(t):
  eqtype = {
      'F' : "Fencing",
      'H' : "Heavy",
      'K' : "Curved",
      'S' : "Straight",
      'D' : "Dodging",
      'B' : "Blocking",
      'P' : "Parrying",
      'G' : "Guarding"
      }
  if not t in eqtype:
    raise Exception("Invalid equipment type {}".format(t))
  return eqtype[t]


def equip_strength_str(s):
  if s == "S":
    return "*"
  return s


def equip_spec_str(e):
  return "{} : {}".format(
      equip_type_str(e['type']),
      equip_strength_str(e['strength'])
      )


def hud(p1, p2, col = 60):
  # names
  name1 = p1['name']
  name2 = right_just(
      "{}".format(p2['name']),
      col = col - len(name1)
      )
  # equipment
  w1 = p1['weapon']
  w2 = p2['weapon']
  a1 = p1['armor']
  a2 = p2['armor']
  ws1 = w1['name'] + " (" + equip_spec_str(w1) + ")"
  as1 = a1['name'] + " (" + equip_spec_str(a1) + ")"
  ws2 = right_just(
      w2['name'] + " (" + equip_spec_str(w2) + ")",
      col = col - len(ws1)
      )
  as2 = right_just(
      a2['name'] + " (" + equip_spec_str(a2) + ")",
      col = col - len(as1)
      )
  # hp
  hp1 = "HP: {}".format(p1['hp']) 
  hp2 = right_just(
      "HP: {}".format(p2['hp']),
      col = col - len(hp1)
      )

  msg = "{}{}\n{}{}\n{}{}\n{}\n{}{}"
  return msg.format(
      name1, name2,
      ws1, ws2,
      as1, as2,
      hp_bar(p1['hp'], p2['hp'], col = col),
      hp1, hp2
      )
def test_hud(col = 60):
  p1 = keyboard_warrior()
  equip_weapon(p1,rapier)
  equip_armor(p1,leather)
  p2 = computer_bug()
  equip_weapon(p2,buster_sword)
  equip_armor(p2,plate_mail)
  for x in range(195, 0, -5):
    p1['hp'] = x
    p2['hp'] = 200 - x
    print(hud(p1,p2,col))
    print()

def a_str(a):
  atype = {
      'S' : 'Strike',
      'T' : 'Thrust',
      'L' : 'Lash'
      }
  return "{} {}".format(atype[a['type']], a['strength'])

def d_str(d):
  dtype = {
      'D' : 'Dodge',
      'P' : 'Parry',
      'B' : 'Block'
      }
  return "{} {}".format(dtype[d['type']], d['strength'])

def play_by_play(dmg, aname, dname, attack, defense):
  action_msg = "{} attacks with {}...\n{} defends with {}--{}!".format(
      aname,
      a_str(attack),
      dname,
      d_str(defense),
      hit_or_miss(dmg)
      )
  ds = dmg
  if dmg == 0:
    ds = "NO"
  dmg_msg = "{} takes {} damage!".format(dname, ds)
  return "{}\n{}".format(action_msg, dmg_msg)

def test_play_by_play():
  fatalina = make_player("Fatalina")
  fjoao = make_player("Fjoao")
  equip_weapon(fatalina, buster_sword)
  equip_armor(fatalina, plate_mail)
  equip_weapon(fjoao, rapier)
  equip_armor(fjoao, leather)
  a1 = {
      'type' : 'S',
      'strength' : 9
      }
  d1 = {
      'type' : 'P',
      'strength' : 1
      }
  dmg = damage(
      a1['type'],
      d1['type'],
      a1['strength'],
      d1['strength'],
      fatalina['weapon']['type'],
      fatalina['weapon']['strength'],
      fjoao['armor']['type'],
      fjoao['armor']['strength'])
  print(play_by_play(dmg, fatalina['name'], fjoao['name'], a1, d1))
  a2 = {
      'type' : 'T',
      'strength' : 9
      }
  d2 = {
      'type' : 'P',
      'strength' : 1
      }
  dmg = damage(
      a2['type'],
      d2['type'],
      a2['strength'],
      d2['strength'],
      fjoao['weapon']['type'],
      fjoao['weapon']['strength'],
      fatalina['armor']['type'],
      fatalina['armor']['strength'],
      )
  print(play_by_play(dmg, fjoao['name'], fatalina['name'], a2, d2))
  print(hud(fatalina,fjoao))
  
def select_card_i(cards, subdeck = "attack"):
  hands = cards
  hand = cards[subdeck]
  assert type(hand) == list 
  lookup = {
      'attack' : 'Attack',
      'defense' : 'Defense',
      }
  print("### {} Cards ###".format(lookup[subdeck]))
  card_lines = display_hand(hand)
  if len(card_lines) == 0:
    print("No cards in hand!")
    return None, hands
  # print out hand
  print("\n".join(card_lines))
  # get selection
  response = ""
  options = [str(i) for i in range(1,len(card_lines)+1)]
  while not response in options:
    response = input("Select a card (1-{}) ".format(len(card_lines))).strip()
  return int(response)-1

def select_action(p, action_type) -> int:
  if not action_type in ["attack", "defense", "special"]:
    raise Exception("Invalid action type: {}".format(action_type))
  return select_card_i(p['cards'], subdeck = action_type)

def cpu_action(cp, action_type, method = 0) -> int:
  if not action_type in ["attack", "defense", "special"]:
    raise Exception("Invalid action type: {}".format(action_type))
  if method == 0:
    if action_type == "special":
      return None
    return 0

def run_duel(player, cpu_player, order = 1, cpu_method = 0, events = False,
    col = 70, debug = False):
  plr = player_copy(player)
  opp = player_copy(cpu_player)
  
  PLR = 1
  OPP = 2
  d = make_duel(plr, opp, order = order)
  deck = d['deck']
  for r in range(10):
    print()
    print("\n" + "=" * 60)
    print(" ROUND {}/10".format(d['round']))
    print("\n" + "=" * 60)
    print()
    print(hud(plr, opp, col = col))
    print()
    # draw phase
    plr['cards'], deck = draw_hands(plr['cards'], deck)
    opp['cards'], deck = draw_hands(opp['cards'], deck)
    # event phase todo:event
    # - select special
    duel_select_events(d) # todo:events not implemented yet!
    # - run active events - not yet implemented todo:event
    duel_run_events(d, None) # todo:events not implented yet
    for t in range(2):
      # turn start 
      if duel_current_attacker(d) == PLR:
        plr_action_type = "attack"
        opp_action_type = "defense"
        sign = 1
      else:
        plr_action_type = "defense"
        opp_action_type = "attack"
        sign = -1
      # action selection
      opp_a = cpu_action(opp, opp_action_type, method = cpu_method)
      duel_run_events(d, None) # todo:events not implemented yet
      plr_a = select_action(plr, plr_action_type)
      if duel_current_attacker(d) == PLR:
        a_i = plr_a
        d_i = opp_a
      else:
        a_i = opp_a
        d_i = plr_a

      # we need to do this before selecting the attack because the
      # game model will update the current attacker
      aname = plr['name'] if duel_current_attacker(d) == PLR else opp['name']
      dname = plr['name'] if duel_current_attacker(d) == OPP else opp['name']
 
      dmg, attack, defense = duel_select_attack_defense(
          d,
          duel_current_attacker(d),
          a_i,
          d_i
          )
      # display actions taken and damage
      print()
      print(play_by_play(dmg, aname, dname, attack, defense))
      print()
      print(hud(plr,opp, col = col))
      print()

      if debug:
        dump = "round={}; round_status={}; current_attacker={}".format(
            d['round'],
            duel_round_status(d),
            duel_current_attacker(d)
            )
        print(dump)

      # check for duel status
      if duel_status(d):
        break
    print()
    x = input("Press enter to continue...")
    if duel_status(d):
      break

  print()
  # announce duel status
  if duel_winner(d) == PLR:
    msg = "YOU WIN: You, {}, defeated {} in {} rounds."
  elif duel_winner(d) == OPP:
    msg = "YOU LOSE: You, {}, were defeated by {} in {} rounds."
  else:
    msg = "DRAW: You, {}, failed to defeat {} in {} rounds, resulting in a draw."
  print()
  print(msg.format(
      plr['name'],
      opp['name'],
      d['round'],
      ))
  print()
  return duel_status(d)

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

def test_hud2(col = 70):
  you = make_player("WYAN")
  wapier = clone_equipment(rapier)
  wapier['name'] = "WAPIER"
  pwate = clone_equipment(plate_mail)
  equip_weapon(you,wapier)
  equip_armor(you,pwate)

  enemy = make_player("Garbage Dragon Emperor")
  sickle = make_weapon("Reaping Sickle",'K','S')
  garmor = make_armor("Demonic Garbage Armor", 'B', 'S')
  equip_weapon(enemy,sickle)
  equip_armor(enemy,garmor)
  print(hud(you, enemy, col = col))

def wyan_vs_gdragon(debug = False) -> int:

  you = make_player("WYAN")
  wapier = clone_equipment(rapier)
  wapier['name'] = "WAPIER"
  pwate = clone_equipment(plate_mail)
  equip_weapon(you,wapier)
  equip_armor(you,pwate)

  enemy = make_player("Garbage Dragon Emperor")
  sickle = make_weapon("Reaping Sickle",'K','S')
  garmor = make_armor("Demonic Garbage Armor", 'B', 'S')
  equip_weapon(enemy,sickle)
  equip_armor(enemy,garmor)

  print("Your name is WYAN.")
  print("Your weapon is a WAPIER (Fencing Class B)")
  print("You are wearing PWATE MAIW ARMOR (Blocking Class A)")
  print()
  x = input("Press enter to continue...")
  print()
  print("Your opponent is the GARBAGE DRAGON EMPEROR.")
  print("His weapon of choice is a REAPING SICKLE (Curved Class *)")
  print("He is wearing DEMONIC GARBAGE ARMOR (Blocking Class *)")
  print()
  print("You have 10 rounds to defeat him in a DUEL!")
  print("It will be a difficult battle, but you must not lose spirit.")
  print()
  x = input("Press enter to begin...")
  print()
  
  col = 70
  result = run_duel(you,enemy,order = 1, cpu_method = 0,
      events = False, col = col, debug = debug)
  print()
  x = input("[Press enter]")
  return result

def run_the_duels(debug = False):
  scenarios = {
      "WYAN vs Emperor Garbage Dragon (No events)" : wyan_vs_gdragon,
      "Exit" : None
      }
  scenario_names = list(scenarios.keys())
  options = [str(i) for i in range(1,len(scenarios)+1)]
  choices = ["{}) {}".format(options[i], scenario_names[i]) for i in range(len(scenarios))]
  menu = "Duel Simulator\n==============\n\n{}".format("\n".join(choices))
  while (1):
    response = None
    while not response in options:
      screen_clear()
      print(menu)
      response = input("Select a scenario (1-{}) ".format(len(scenarios)))
      screen_clear()
    selection = scenario_names[int(response)-1]
    if selection == "Exit":
      exit()
    else:
      f = scenarios[selection]
      result = f(debug = debug)
