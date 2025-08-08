import random

MAX_ROUNDS = 30
MAX_HAND_SIZE = 6

def make_deck(n):
    deck = []
    for i in range(1, n + 1):
        deck += [i] * i
    return(deck)



class Deck:
    def __init__(self, n):
        self.draw = make_deck(n)
        self.discard = []
        random.shuffle(self.draw)

    def __str__(self):
        return("Draw Pile: " + str(self.draw) + "\n" + "Discard Pile: " + str(self.discard))

    def replenish(self):
        random.shuffle(self.discard)
        self.draw = self.discard
        self.discard = []

    def deal(self):
        if self.draw == []:
            self.replenish()
        return(self.draw.pop(0))
    
    def discard_hand(self, hand):
        self.discard += hand

class Agent:
    def __init__(self, policy):
        self.policy = policy

    def play(self, goal, n):
        deck = Deck(n)
        points = 0
        hand = []
        round = 0
        while points < goal and round < MAX_ROUNDS:
            move = self.policy(deck, hand, goal, n, points)
            if move == "HIT":
                new_card = deck.deal()
                if new_card in hand:
                    deck.discard_hand(hand)
                    deck.discard_hand([new_card])
                    round += 1
                    # print("Busted with hand " + str(hand + [new_card]))
                    hand = []
                else:
                    hand += [new_card]
                    if len(hand) == MAX_HAND_SIZE:
                        # print("Maxed out hand size with hand" + str(hand))
                        points += sum(hand)
                        deck.discard_hand(hand)
                        hand = []
                        round += 1

            if move == "STAY":
                points += sum(hand)
                deck.discard_hand(hand)
                # print("Stayed with hand " + str(hand))
                hand = []
                round += 1

        return(round)
    
    def average_length(self, goal, n, nsims):
        avg_length = 0
        for sim in range(nsims):
            avg_length += self.play(goal, n)
        return(avg_length / nsims)
"""
small_deck = Deck(6)
print(small_deck)
hand = []
for k in range(5):
    hand.append(small_deck.deal())
print("Hand: " + str(hand))
print(small_deck)"""

def cheat(deck, hand, goal, n, points):
    if len(deck.draw) > 0 and deck.draw[0] not in hand: return("HIT")
    else: return("STAY")

def draw_x(x):
    def f(deck, hand, goal, n, points):
        if len(hand) < x: return("HIT")
        else: return("STAY")
    return(f)

def random_move(deck, hand, goal, n, points):
    if random.random() > .5: return("HIT")
    else: return("STAY")

def sum_thresh(x):
    def f(deck, hand, goal, n, points):
        if sum(hand) < x: return("HIT")
        else: return("STAY")
    return(f)

def ev_thresh_no_memory(x):
    def f(deck, hand, goal, n, points):
        fake_deck = make_deck(n)
        for card in hand:
            fake_deck.remove(card)
        if sum([card for card in fake_deck if card not in hand]) / len(fake_deck) > x: return("HIT")
        else: return("STAY")
    return(f)

def ev_thresh_with_memory(x):
    def f(deck, hand, goal, n, points):
        if len(deck) == 0:
            fake_deck = make_deck(n)
            for card in hand:
                fake_deck.remove(card)
            if sum([card for card in fake_deck if card not in hand]) / len(fake_deck) > x: return("HIT")
            else: return("STAY")

        if sum([card for card in deck if card not in hand]) / len(deck) > x: return("HIT")
        else: return("STAY")
    return(f)


def risk_thresh_with_memory(p):
    def f(deck, hand, goal, n, points):
        if len(deck.draw) == 0:
            p_bust = len([card for card in deck.discard if card in hand]) / len(deck.discard)
        else:
            p_bust = len([card for card in deck.draw if card in hand]) / len(deck.draw)
        if p_bust <= p: return("HIT")
        else: return("STAY")
    return(f)

cheater = Agent(cheat)
singler = Agent(draw_x(1))
doubler = Agent(draw_x(2))
tripler = Agent(draw_x(3))
chaos = Agent(random_move)

#print(chaos.average_length(30,6, 100000))

for thresh in range(2, 20):
    avg = Agent(sum_thresh(thresh)).average_length(60, 6, 1000)
    print("At threshhold of " + str(thresh) + ", on average " + str(avg) + " moves are required.")

def optimal_thresh(goal, n, nsims):
    best_avg = goal
    best_thresh = -1
    for thresh in range(2, sum(range(n))):
        avg = Agent(sum_thresh(thresh)).average_length(goal, n, nsims)
        if avg < best_avg:
            best_avg = avg
            best_thresh = thresh
    return(best_thresh)
    
"""print(optimal_thresh(60, 6, 5000))
print(optimal_thresh(200, 12, 100))
print(Agent(sum_thresh(27)).average_length(200, 12, 1000))"""

for p_thresh in [i/100 for i in range(20, 40)]:
    avg = Agent(risk_thresh_with_memory(p_thresh)).average_length(200, 12, 1000)
    print("At risk threshhold of " + str(p_thresh) + ", on average " + str(avg) + " moves are required.")