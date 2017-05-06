from deck import Shoe
from player import Player
from hand import Hand

# Constants
INITIAL_BALANCE = 100
MINIMAL_BET = 1

# Globals
dealer_hand = Hand(Player("Dealer", None), None)
active_players = [Player("Player1", INITIAL_BALANCE)]
shoe = Shoe(6)

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
