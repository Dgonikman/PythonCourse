from deck import Shoe
from player import Player
from hand import Hand, State

# Constants
INITIAL_BALANCE = 100
MINIMAL_BET = 1

# Globals
dealer_hand = Hand(Player("Dealer", None), None)
active_players = [Player("Player1", INITIAL_BALANCE)]
shoe = Shoe(6)


def print_hand():
    print
    print dealer_hand
    print hand
    print playing_hand.Player.Name + ", what do you do?"


while len(active_players) > 0:
    # Init round
    active_hands = []
    finished_hands = []
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

    # Gameplay
    while len(active_hands) > 0:
        playing_hand = active_hands.pop(0)

        while playing_hand.Status == State.Active:
            print_hand()
            action = raw_input("(S)tand\(H)it: ")
            if action == 'S' or action == 's':
                print "You chose to stand"
                playing_hand.Status = State.Stand
            elif action == 'H' or action == 'h':
                print "You chose to hit"
                playing_hand.deal(shoe.pop())
                if playing_hand.value == 21:
                    print "21! Your'e done"
                    playing_hand.Status = State.Stand
                elif playing_hand.value > 21:
                    print str(playing_hand.value) + ". Your hand is dead, sir"
                    playing_hand.Status = State.Bust
            else:
                print "Illegal move, try again."

        finished_hands.append(playing_hand)

    # Show dealers' hand
    dealer_hand.Cards[0].flip()
    print
    print dealer_hand

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
