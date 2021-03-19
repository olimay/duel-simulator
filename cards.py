# cards

import random

MAX_HAND = 6
MAX_SPECIAL = 3

# cards
def make_hand(attack_cards = None, defense_cards = None, special_cards = None) -> dict:
  # cards
  cards = {} 
  #  attack
  cards['attack'] = [] if attack_cards is None else attack_cards
  #  defense
  cards['defense'] = [] if defense_cards is None else defense_cards
  #  special
  cards['special'] = [] if special_cards is None else special_cards
  return cards

def subhand_copy(ad_hand) -> list:
  # assuming a list of shallow dicts
  return [c.copy() for c in ad_hand]

def hand_copy(cards) -> dict: 
  cards_copy = {}
  # attack
  cards_copy['attack'] = subhand_copy(cards['attack'])
  #  defense
  cards_copy['defense'] = subhand_copy(cards['defense'])
  #  special
  cards_copy['special'] = subhand_copy(cards['special'])
  return cards_copy

def make_attack_card(attack_type : str, attack_strength : int) -> dict:
  if not attack_type in ['S','T','L']:
    raise Exception("can't make card: invalid attack card type: {}/{}".format(attack_type, attack_strength))
  if attack_strength < 1 or attack_strength > 9:
    raise Exception("can't make card: invalid attack card strength: {}".format(attack_type, attack_strength))
  return {'type' : attack_type, 'strength' : attack_strength}

def make_defense_card(defense_type : str, defense_strength : int) -> dict:
  if not defense_type in ['D','P','B']:
    raise Exception("can't make card: invalid defense card type: {}/{}".format(defense_type, defense_strength))
  if defense_strength < 1 or defense_strength > 9:
    raise Exception("can't make card: invalid defense card strength: {}".format(defense_type, defense_strength))
  return {'type' : defense_type, 'strength' : defense_strength}

def is_attack_card(c):
  a_types = ['S','T','L']
  return c['type'] in a_types

def is_defense_card(c):
  d_types = ['D','P','B']
  return c['type'] in d_types

def make_deck() -> dict:
  attack_deck = []
  defense_deck = []
  special_deck = []

  # card generation
  # each strength level repeated four times, with (3, 7) for a fifth time
  strengths = [x for x in range(1,9)] * 4 + [x for x in range(3, 7)]
  a_types = ['S','T','L']
  d_types = ['D','P','B']
  for a in a_types:
    cards = [make_attack_card(a, s) for s in strengths]
    attack_deck += cards

  random.shuffle(attack_deck)

  for d in d_types:
    cards = [make_defense_card(d, s) for s in strengths]
    defense_deck += cards
  random.shuffle(defense_deck)

  return { 'attack' : attack_deck, 'defense' : defense_deck }

def card_name(card : dict) -> str:
  return "{}{}".format(card['type'], card['strength'])

def draw_card(deck, subdeck = "attack") -> tuple:
  if len(deck[subdeck]) == 0:
    return (None, deck)
  card = deck[subdeck].pop()
  return (card, deck)

def test_draw_card():
  deck = make_deck()
  for i in range(1, 10):
    hand = []
    for j in range(1, 8):
      card, deck = draw_card(deck, "attack")
      # print(card)
      hand += [card]
    # print(hand)
    debug_print_hand(hand)

def debug_print_hand(hand, name):
  return("hand {} : {}".format(name, [card_name(c) for c in hand]))

def draw_hand(hand, deck, subdeck, max_cards = MAX_HAND):
  h = hand
  d = deck
  for i in range(len(hand),max_cards):
    c, d = draw_card(d, subdeck) 
    if not c is None:
      h += [c]
    else:
      break
  return h, d

def card_to_str(card : dict, lookup = None):
  if lookup is None:
    lookup = {
        'S' : 'Strike',
        'T' : 'Thrust',
        'L' : 'Lash',
        'D' : 'Dodge',
        'P' : 'Parry',
        'B' : 'Block',
        }
  return "{} Strength {}".format(lookup[card['type']], card['strength'])

def test_draw_hand():
  h1 = []
  h2 = []
  d = make_deck()
  h1, d = draw_hand(h1, d, "defense", MAX_HAND) 
  h2, d = draw_hand(h2, d, "attack", MAX_HAND) 
  print("MAX_HAND={}\n{}\n{}".format(
      MAX_HAND,
      debug_print_hand(h1,"defense hand"),
      debug_print_hand(h2, "attack_hand")
    ))
  print("{}".format(d))
  
def draw_hands(hands = None, deck = None, max_attack = MAX_HAND, max_defense = MAX_HAND, max_special = MAX_SPECIAL):
  d = deck
  c = hands
  if d is None:
    # generate a new deck
    d = make_deck()
  if c is None:
    c = make_hand()
  hands_max = {'attack': max_attack, 'defense': max_defense}
  for kind in ["attack","defense"]:
    # print("kind: {}".format(kind))
    c[kind], d = draw_hand(c[kind], d, kind,max_cards=hands_max[kind])
  return c, d

def test_draw_hands():
  cards, d = draw_hands(hands=None,deck=None,max_attack=4,max_defense=5,max_special=0)
  print("MAX_HAND={}\n{}\n{}".format(
      MAX_HAND,
      debug_print_hand(cards["defense"],"defense hand"),
      debug_print_hand(cards["attack"], "attack_hand")
    ))
  print("{}".format(d))

def display_hand(hand : list):
  cards_str = [card_to_str(c) for c in hand]
  lines = []
  for i in range(len(cards_str)):
    lines += ["{}) {}".format(i+1, cards_str[i])]
  return lines 

def select_card(cards, subdeck = "attack"):
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
    response = input("Select a card (1-{})".format(len(card_lines)))
  card = hand.pop(int(response)-1)
  hands[subdeck] = hand
  return card, hands 

def test_select_card():
  deck = make_deck()
  cards, deck = draw_hands(hands=None, deck=deck,max_attack = 5, max_defense=3,max_special=0)
  print(cards['attack'])
  for i in range(10):
    c, cards = select_card(cards, subdeck = "attack")
    assert type(cards) == dict
    if not c is None:
      print("Selected attack: {}".format(card_to_str(c)))
    else:
      print("Couldn't draw attack card!")
    c, cards = select_card(cards, subdeck = "defense")
    assert type(cards) == dict
    if not c is None:
      print("Selected defense: {}".format(card_to_str(c)))
    else:
      print("Couldn't draw attack card!")
    cards, deck = draw_hands(hands=cards, deck=deck,max_attack = 5, max_defense=3,max_special=0)

# test_draw_card()
# test_draw_hand()
# test_draw_hands()
# test_select_card()
