# duel.py

from cards import *
from damage import *
from player import *
from weaponsarmor import *

def make_duel(player_1 : dict, player_2 : dict, max_rounds = 10, order = 1, deck = None):
  # initializes a duel game model with the specified players
  # and specified maxiumum number of rounds
  d = {}
  d['round'] = 1
  d['order'] = order if order in [1,-1] else 1
  d['events'] = [] # empty array for active events
  d['phase'] = -1
  
  # starting parameters
  d['p1'] = player_1
  d['p2'] = player_2
  d['__max_rounds'] = max_rounds

  # check for deck to use
  d['deck'] = deck
  if deck is None:
    d['deck'] = make_deck()

  d['history'] = []

  # actions taken
  d['act_p1'] = []
  d['act_p2'] = []
  
  return d

# accessors for static fields
def duel_max_rounds(d):
  return d['__max_rounds']

# status functions

## win/loss/draw/continue status
def duel_status(d):
  # returns
  # which player (1,2) has won
  # 0 if the duel is not yet over (continue)
  # 3 if the duel is a draw
  # note that the duel ends *immediately* when hp falls to zero
  if d['p1']['hp'] <= 0:
    return 2
  if d['p2']['hp'] <= 0:
    return 1
  if d['round'] > duel_max_rounds(d):
    return 3
  return 0

def duel_winner(d):
  # returns which player (1,2) has won
  # or 0 if the duel is not yet over or if the duel is a draw
  status = duel_status(d)
  if status in (1,2):
    return status
  return 0

def duel_is_draw(d):
  # returns true if the current dual is over and a draw
  return duel_status(d) == 3

def duel_winner_info(d):
  # returns player dict of winning player
  # or None if the duel is not yet over, or if the winner is a draw
  winner = duel_winner(d)
  if winner == 0:
    return None
  if winner == 1:
    return d['p1']
  return d['p2']

## round status/management
def duel_round_status(d):
  # 0 not started: zero turns have resolved
  # 1 incomplete: one turn has resolved
  # 2 complete: both turns have resolved
  actions = len(d['act_p1']) + len(d['act_p2'])
  if actions == 4:
    return 2
  elif actions >= 2:
    return 1
  return 0

def duel_turn(d):
  status = duel_round_status(d)
  phase = d['phase']
  return status + 1 if phase >= 0 and status else 0

def duel_build_history(d):
  # copies attibutes of the current duel round to a new dict
  info = {}

  # don't need to be stored: duel_max_rounds, phase, deck (deck saved at the end)

  # strings and scalars
  info['order'] = d['order']
  info['round'] = d['round']

  info['events'] = d['events'].copy()
  # player state
  info['p1'] = player_copy(d['p1'])
  info['p2'] = player_copy(d['p2'])
  # action information
  info['act_p1'] = d['act_p1'].copy()
  info['act_p2'] = d['act_p2'].copy()
  return info

def duel_new_round(d):
  # Increment the round count, record the current round in the history,
  # clear the round fields.
  #
  # check to see if the game has already ended
  if duel_status(d):
    msg = ("Error: attempted new round of duel that is over\n" +
        "status={}, round={}/max_rounds={}"
        )
    raise Exception(msg.format(duel_status(d), d['round'], duel_max_rounds(d)))
  # check to see if round is actually over
  if duel_round_status(d) < 2:
    msg = (
        "Error: attempt to start a new round " +
        "before both players take actions\n" +
        "round={} status={}")
    raise Exception(msg.format(d['round'], duel_round_status(d)))

  d['history'] += [duel_build_history(d)]
  # if we've exceeded max rounds it's up to the controller to end the game
  d['round'] += 1 

  # if the duel is continuing
  if not duel_status(d):
    # reset round info
    d['turn'] = 0
    d['phase'] = -1
    d['act_p1'] = []
    d['act_p2'] = []
    # todo:event decrement event countdown

## actions
def duel_current_attacker(d):
  #
  if duel_status(d) or d['phase'] < 0 or duel_round_status(d) == 2:
    return 0

  if d['order'] != -1 and d['order'] != 1:
    msg = "Invalid order {}, should be -1 or 1" + " (round={} phase={})"
    raise Exception(msg.format(d['order'], d['round'], d['phase']))
  players = [None,1, 2]
  return players[d['order']+d['order']*duel_round_status(d)]


def duel_select_events(d, p1_hand_index = None, p2_hand_index = None):
  # will figure out how to implement events later on
  # right now this just increments the phase
  if d['phase'] >= 0:
    msg = "Event phase completed for this round; expected phase=-1, phase={}"
    raise Exception(msg.format(d['phase']))
  # todo:event
  d['events'] = []
  d['phase'] = 0

def duel_run_events(d : dict, callbacks : dict):
  # print("Warning: event system not implemented! Skipping events.")
  pass


def duel_select_attack_defense(d, attacker : int, a_card_i : int, d_card_i):
  # register an attack and defense, modify the player hp
  # return damage done to defender
  # --
  # make sure we are in the right phase
  if d['phase'] < 0:
    msg = "Not yet in attack/defense phase (>= 0); phase={}"
    raise Exception(msg.format(d['phase']))
  #
  # next sanity check to make sure a player doesn't attack twice in a round
  # or that an attack is registered after both players have taken their turns
  if duel_round_status(d) == 2:
    msg = "Round is complete; players have taken their turns: {} {} order={}" 
    raise Exception(msg.format(d['act_p1'], d['act_p2'], d['order']))
  if duel_round_status(d) == 1:
    if d['order'] > 0 and attacker == 1:
      msg = "P1 already attacked/P2 already defended this turn: {} {} order={}" 
      raise Exception(msg.format(d['act_p1'], d['act_p2'], d['order']))
    elif d['order'] < 0 and attacker == 2:
      msg = "P2 already attacked/P1 already defended this turn: {} {} order={}" 
      raise Exception(msg.format(d['act_p2'], d['act_p1'], d['order']))
  # get set variables based on who is the attacker and defender
  if attacker == 1:
    a_plr = d['p1']
    d_plr = d['p2']
    a_act = d['act_p1']
    d_act = d['act_p2']
  else:
    a_plr = d['p2']
    d_plr = d['p1']
    a_act = d['act_p2']
    d_act = d['act_p1']
  a_cards = a_plr['cards']['attack']
  d_cards = d_plr['cards']['defense']

  # Do we even have cards?
  if len(a_cards) <= 0 or len(d_cards) <= 0:
    # what is going on
      msg = "Not enough attack or defense cards! Attack={} Defense={}" 
      raise Exception(msg.format(a_cards, d_cards))

  # make sure the card index is in bounds: 0 < i < len(hand)
  if a_card_i < 0 or a_card_i >= len(a_cards):
      msg = "Invalid attack card index {}; attack cards {}" 
      raise Exception(msg.format(a_card_i, a_cards))
  if d_card_i < 0 or d_card_i >= len(d_cards):
      msg = "Invalid defense card index {}; defense cards {}" 
      raise Exception(msg.format(d_card_i, d_cards))

  # get attack and defense cards from the hands
  attack = a_cards.pop(a_card_i)
  defense = d_cards.pop(d_card_i)

  dmg = damage(
      attack['type'],
      defense['type'],
      attack['strength'],
      defense['strength'],
      a_plr['weapon']['type'],
      a_plr['weapon']['strength'],
      d_plr['armor']['type'],
      d_plr['armor']['strength'])

  # resolve damage
  a_plr['hp'] += dmg
  d_plr['hp'] -= dmg

  # log actions
  a_act += [attack]
  d_act += [defense]
  
  # increment phase
  d['phase'] += 1

  if not duel_status(d) and duel_round_status(d) == 2:
    duel_new_round(d)

  return dmg, attack, defense


def hit_or_miss(dmg):
  return "HIT" if dmg > 0 else "MISS"

def test_duel_select_attack_defense():

  plr_A = make_player("Cloud Strife")
  equip_weapon(plr_A, buster_sword) 
  equip_armor(plr_A, plate_mail)
  plr_B = make_player("Carmine Ragussa")
  equip_weapon(plr_B, rapier)
  equip_armor(plr_B, leather)
  # 
  d = make_duel(plr_A, plr_B)
  deck = d['deck']
  plr_A['cards'], deck = draw_hands(plr_A['cards'], deck)
  plr_B['cards'], deck = draw_hands(plr_B['cards'], deck)
  msg = "{} attacks with {}{} and {} defends with {}{}, for {} dmg - {}"

  print("Current attacker: player {}".format(duel_current_attacker(d)))
  dmg, a_card, d_card = duel_select_attack_defense(d, 1, 0, 0)
  print(msg.format(
    plr_A['name'], a_card['type'], a_card['strength'],
    plr_B['name'], d_card['type'], d_card['strength'],
    dmg, hit_or_miss(dmg)))
  msg2 = "HP: {}={} {}={}"
  print(msg2.format(
    plr_A['name'], plr_A['hp'],
    plr_B['name'], plr_B['hp'],
    ))

  print("Current attacker: player {}".format(duel_current_attacker(d)))
  dmg, a_card, d_card = duel_select_attack_defense(d, 2, 0, 0)
  print(msg.format(
    plr_B['name'], a_card['type'], a_card['strength'],
    plr_A['name'], d_card['type'], d_card['strength'],
    dmg, hit_or_miss(dmg)))
  msg2 = "HP: {}={} {}={}"
  print(msg2.format(
    plr_A['name'], plr_A['hp'],
    plr_B['name'], plr_B['hp'],
    ))

def test_duel_new_round(n = 2) -> dict:
  plr_A = make_player("Bjoao Phranko")
  equip_weapon(plr_A, rapier) 
  equip_armor(plr_A, plate_mail)
  plr_B = make_player("Gatalina Eroszo")
  equip_weapon(plr_B, buster_sword)
  equip_armor(plr_B, leather)
  # 
  d = make_duel(plr_A, plr_B)
  deck = d['deck']
  msg = "{} attacks with {}{} and {} defends with {}{}, for {} dmg - {}"

  for i in range(n):
    assert i + 1 == d['round'], "round={}, expected {}".format(d['round'], i+1)
    print("Round {}/{}".format(d['round'],duel_max_rounds(d)))
    plr_A['cards'], deck = draw_hands(plr_A['cards'], deck)
    plr_B['cards'], deck = draw_hands(plr_B['cards'], deck)

    print("Skipping event phase...")
    duel_select_events(d)

    print("Current attacker: player {}".format(duel_current_attacker(d)))
    dmg, a_card, d_card = duel_select_attack_defense(d, 1, 0, 0)
    print(msg.format(
      plr_A['name'], a_card['type'], a_card['strength'],
      plr_B['name'], d_card['type'], d_card['strength'],
      dmg, hit_or_miss(dmg)))
    msg2 = "HP: {}={} {}={}"
    print(msg2.format(
      plr_A['name'], plr_A['hp'],
      plr_B['name'], plr_B['hp'],
      ))
    if duel_status(d):
      break

    print("Current attacker: player {}".format(duel_current_attacker(d)))
    dmg, a_card, d_card = duel_select_attack_defense(d, 2, 0, 0)
    print(msg.format(
      plr_B['name'], a_card['type'], a_card['strength'],
      plr_A['name'], d_card['type'], d_card['strength'],
      dmg, hit_or_miss(dmg)))
    msg2 = "HP: {}={} {}={}"
    print(msg2.format(
      plr_A['name'], plr_A['hp'],
      plr_B['name'], plr_B['hp'],
      ))
    if duel_status(d):
      break
  print("Duel ending status: {}".format(duel_status(d)))
  return d


