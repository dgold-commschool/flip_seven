import random, math

MAX_ROUNDS = 100000
LOG = True
def tri_root(n):
    return(math.ceil((math.sqrt(1 + 8 * n) - 1) / 2))

def tri(n):
    return(n * (n + 1) // 2)

class Agent:
    def __init__(self, policy):
        self.policy = policy

    def play(self, goal, n, max_hand_size, max_bonus):
        points = 0
        hand = []
        round = 0
        while points < goal and round < MAX_ROUNDS:
            if sum(hand) + points == goal:
                round += 1
                if LOG: print("Round " + str(round) + ": Forced to stay, goal met!")
                break 
            move = self.policy(hand, goal, n, points, max_hand_size, max_bonus)
            if move == "HIT":
                new_card = tri_root(random.randint(1, n * (n + 1) / 2))
                if new_card in hand:
                    round += 1
                    if LOG: print("Round " + str(round) + ": Busted with hand " + str(hand + [new_card]))
                    hand = []
                else:
                    hand += [new_card]
                    if len(hand) == max_hand_size:
                        round += 1
                        if LOG: print("Round " + str(round) + ": Maxed out hand size with hand " + str(hand))
                        points += sum(hand) + max_bonus
                        hand = []
                        

            if move == "STAY":
                points += sum(hand)
                round += 1
                if LOG: print("Round " + str(round) + ": Stayed with hand " + str(hand))
                hand = []
                

        return(round)
    
    def average_length(self, goal, n, nsims, max_hand_size, max_bonus):
        avg_length = 0
        for sim in range(nsims):
            avg_length += self.play(goal, n, max_hand_size, max_bonus)
        return(avg_length / nsims)
"""
small_deck = Deck(6)
print(small_deck)
hand = []
for k in range(5):
    hand.append(small_deck.deal())
print("Hand: " + str(hand))
print(small_deck)"""

def draw_x(x):
    def f(deck, hand, goal, n, points, max_hand_size, max_bonus):
        if len(hand) < x: return("HIT")
        else: return("STAY")
    return(f)

def random_move(deck, hand, goal, n, points, max_hand_size, max_bonus):
    if random.random() > .5: return("HIT")
    else: return("STAY")

def sum_thresh(x):
    def f(hand, goal, n, points, max_hand_size, max_bonus):
        if sum(hand) < x: return("HIT")
        else: return("STAY")
    return(f)


def ev_thresh_with_memory(x):
    def f(hand, goal, n, points, max_hand_size, max_bonus):
        ev = 0
        for k in range(1, n+1):
            if k not in hand:
                if len(hand) + 1 == max_hand_size:
                    ev += (k + max_bonus) * k / tri(n)
                else:
                    ev += k * k / tri(n)
                
        if ev > x: return("HIT")
        else: return("STAY")
    
    return(f)


def risk_thresh(p):
    def f(deck, hand, goal, n, points):
        prob_bust = sum([k if k not in hand else 0 for k in range(1, n +1)])
        if prob_bust <= p: return("HIT")
        else: return("STAY")
    return(f)


if __name__ == "__main__":
    
    singler = Agent(draw_x(1))
    doubler = Agent(draw_x(2))
    tripler = Agent(draw_x(3))
    chaos = Agent(random_move)

    #print(chaos.average_length(30,6, 100000))

    t = Agent(sum_thresh(9))
    print(t.average_length(60, 6, 1, 4, 10))
