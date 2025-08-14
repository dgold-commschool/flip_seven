# Description of Flip 7

Flip 7 is a recent push-your-luck card game: on each turn, players decide to hit (draw a new card) or stay (bank the points for the current round). If a player draws two copies of the same card, they bust, losing all points gained in the round. If a player manages to draw 7 unique cards, they gain a small bonus (15 points), and the round ends for all players. 

The deck has a unique construction: there are 12 cards numbered 12, 11 cards numbered 11, etc. There are also a few unique score modifiers (+2, +4, +6, +8, +10, and x2) that do not count towards the 7 card goal, as well as 3 copies of three action cards (Freeze, Second Chance, and Flip Three).

The goal of the game is to be the first player to reach 200 points. If two or more players manage to meet this goal, the player with the highest score at the end of the last round wins.

## Generalized Flip 7

Generalized Flip 7 makes a few small adjustments to the details above. Namely,

- No Score Modifiers or Action Cards are included in the deck.
- The deck size is parametrized by an integer n giving the highest card value in the deck.
- The goal is parametrized by an integer g > n(n+1)/2.
- The "Flip 7" bonus is parametrized by integers h and b, giving the maximum hand size and bonus respectively.  

In the original game, n = 12, g = 200, h = 7, and b = 15.

## Generalized Roll 7

The state space of Generalized Flip 7 scales super-exponentially with n, as there are (n+1)!n!(n-1)!... deck states. Thus, we also consider a memoryless variant dubbed Generalized Roll 7, in which values are derived from weighted dice rolls instead of card draws. Specifically, each value is drawn from a discrete distribution over \[1, n\] where the probability of rolling k is directly proportional to k. This game is closer to Pig than the original Flip 7, which we hope will lead to a more tractable solution.

## Modes

In addition, we consider two different modes for each game:

- Solitaire (1-player): One player takes as many rounds as needed to reach the goal, with the aim of minimizing the number of rounds needed.
- Competitive (m-player): m players each play the game (using a shared deck in the case of Flip 7), with each player aiming to be the first to reach the goal. If two or more players reach the goal in the same round, the player with the highest total score at the end of that round wins.

# Questions

**For Solitaire Play:**
- As a function of n, g, h, and b, what are the optimal policies for minimizing the expected number of turns needed?
    - How much do these policies differ between Flip 7 and Roll 7?
    - At what thresholds do the qualitative nature of policies change (eg. risky vs safe)?
- Are there heuristic, easily implemented strategies that lead to approximately optimal play?
- What values of h and b lead to the most "interesting" gameplay?

**For Competitive Play:**
- As a function of m, n, g, h, and b, what are the optimal policies for maximizing each player's probability of winning?