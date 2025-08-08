""" A State is a tuple including
- The current score,
- The cards in the player's hand, represented as a 
- The cards remaining in the deck, represented as a tuple (1s, 2s, 3s, etc.)
"""

from itertools import *

def get_all_hands(n, max_hand_size):
    hands = []
    for hand_size in range(0, max_hand_size + 1):
        hands = hands + [list(k) for k in combinations(range(1, n + 1), hand_size)]
    return(hands)

def get_all_decks(n):
    l = [list(range(0, k + 1)) for k in range(1, n + 1)]
    return(list(product(*l)))


def get_all_states(goal, n, max_hand_size):
    all_hands = get_all_hands(n, max_hand_size)
    all_decks = get_all_decks(n)
    return([(score, tuple(hand), deck) for score in range(0, goal + 1) for hand in all_hands for deck in all_decks])

def bump(deck, card):
    d = list(deck)[:]
    d[card - 1] -= 1
    return(tuple(d))

def get(evs, state):
    if state in evs:
        return(evs[state])
    else:
        return(0)
    
def solve(goal, n, max_hand_size, delta):
    states = get_all_states(goal, n, max_hand_size)
    policy = {state: None for state in states}
    evs = {state: goal for state in states}
    max_delta = delta + 1
    nsims = 0
    while max_delta > delta and nsims < 100:
        max_delta = 0
        nsims += 1
        for score in range(goal, -1, -1):
            for hand_size in range(0, max_hand_size + 1):
                for hand in [tuple(k) for k in combinations(range(1, n + 1), hand_size)]:
                    for deck in [tuple(k) for k in get_all_decks(n)]:
                            
                        if score == goal:
                            evs[(score, hand, deck)] = 0

                        elif hand_size == max_hand_size:
                            if sum(deck) == 0:
                                diff = abs(get(evs, (score, hand, deck)) - (1 + get(evs, (score + sum(hand), (), tuple(range(1, n + 1))))))
                                max_delta = max(diff, max_delta)
                                evs[(score, hand, deck)] = 1 + get(evs, (score + sum(hand), (), tuple(range(1, n + 1))))
                            else:
                                diff = abs(get(evs, (score, hand, deck)) - (1 + get(evs, (score + sum(hand), (), deck))))
                                max_delta = max(diff, max_delta)
                                evs[(score, hand, deck)] = 1 + get(evs, (score + sum(hand), (), deck))
                            
                        else:
                            ev_if_hit = 0
                            if sum(deck) == 0:
                                ev_if_stay = 1 + get(evs,(score + sum(hand), (), tuple(range(1, n + 1))))

                                new_deck = [k if k not in hand else k - 1 for k in range(1, n + 1)]
                                for k in range(1, n + 1):
                                    if new_deck[k-1] > 0:
                                        if k in hand:
                                            ev_if_hit += new_deck[k - 1] * (1 + get(evs,(score, (), bump(new_deck, k))))
                                        else:
                                            ev_if_hit += new_deck[k - 1] * get(evs, (score, tuple(sorted(hand + tuple([k]))), bump(new_deck, k)))
                                ev_if_hit = ev_if_hit / sum(new_deck)
                                

                            else:
                                ev_if_stay = 1 + get(evs,(score + sum(hand), (), deck))
                                for k in range(1, n + 1):
                                    if deck[k-1] > 0:
                                        if k in hand:
                                            ev_if_hit += deck[k - 1] * (1 + get(evs, (score, (), bump(deck, k))))
                                        else:
                                            ev_if_hit += deck[k - 1] * get(evs, (score, tuple(sorted(hand + tuple([k]))), bump(deck, k)))
                                ev_if_hit = ev_if_hit / sum(deck)
                                if ev_if_hit == 0:
                                    quit()
                                    
                            diff = abs(evs[(score, hand, deck)] - min(ev_if_hit, ev_if_stay))
                            max_delta = max(diff, max_delta)
                            
                            evs[(score, hand, deck)] = min(ev_if_hit, ev_if_stay)
                            if ev_if_hit < ev_if_stay:
                                policy[(score, hand, deck)] = "Hit"
                            else:
                                policy[(score, hand, deck)] = "Stay"
        print(nsims, max_delta)
    return(evs[(0, (), tuple(range(1, n+1)))])

print(solve(20, 6, 2, 1))
