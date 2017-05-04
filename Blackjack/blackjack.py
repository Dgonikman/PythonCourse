from deck import Shoe
from player import Player

# Constants
INITIAL_BALANCE = 100
MINIMAL_BET = 1

# Globals
dealer_hand = Hand(Player("Dealer", None), None)
active_players = [Player("Player1", INITIAL_BALANCE)]
shoe = Shoe(6)


class Hand(object):
    def __init__(self, current_player, bet):
        self.Player = current_player
        self.Bet = bet
        self.Cards = []

    @property
    def value(self):
        return len(self)

    def __str__(self):
        return str(self.Player.Name) + ',' + str(self.Bet) + ':' +\
               ''.join(map(str, self.Cards)) + ' Value: ' + str(self.value)

    def __len__(self):
        # should be value of the cards
        return len(self.Cards)


while len(active_players) > 0:
    # Init round
    active_hands = []
    for player in active_players:
        active_hands.append(Hand(player, MINIMAL_BET))
    print 'Active Hands: {hands}'.format(hands=len(active_hands))

    # Deal hands
    for _ in xrange(0, 2):
        for hand in active_hands:
            hand.deal(shoe.pop())
        dealer_hand.deal(shoe.pop())
    dealer_hand.Cards[0].flip()

    # Print hands
    print
    print dealer_hand
    for hand in active_hands:
        print hand

    # Pay
    for player in active_players:
        player.Balance -= player.Balance

    # Check remaining cash
    bankrupt_players = [player for player in active_players if player.Balance <= 0]
    active_players = [player for player in active_players if player.Balance > 0]

    print
    for player in bankrupt_players:
        print player.Name + " is bankrupt!"

print "Game over! House always wins!"
