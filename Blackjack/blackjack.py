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
def play_hand(hand_to_play, action):
    player_name = hand_to_play.Player.Name
    if action == 'S' or action == 's':
        print player_name + " chose to stand"
        hand_to_play.Status = State.Stand
    elif action == 'H' or action == 'h':
        print player_name + " chose to hit"
        hand_to_play.deal(shoe.pop())
        print hand_to_play
        if hand_to_play.value == 21:
            print "21! " + player_name + ", your'e done"
            hand_to_play.Status = State.Stand
        elif hand_to_play.value > 21:
            print str(hand_to_play.value) + ". Your hand is dead, " + player_name
            hand_to_play.Status = State.Bust
    elif action == 'D' or action == 'd':
        print "Not supported yet."
    else:
        print "Illegal move, try again."


def pay_players():
    blackjack_hands = [played_hand for played_hand in finished_hands if played_hand.Status == State.BlackJack]
    bust_hands = [played_hand for played_hand in finished_hands if played_hand.Status == State.Bust]
    stand_hands = [played_hand for played_hand in finished_hands if played_hand.Status == State.Stand]

    for bust_hand in bust_hands:
        bust_hand.Player.Balance -= bust_hand.Bet
        print bust_hand

    for blackjack_hand in blackjack_hands:
        blackjack_hand.Player.Balance += 1.5 * blackjack_hand.Bet
        print blackjack_hand

    for stand_hand in stand_hands:
        if dealer_hand.Status == State.Bust:
            stand_hand.Player.Balance += stand_hand.Bet
        else:  # Dealer Stand or Blackjack
            if stand_hand.value == dealer_hand.value:
                stand_hand.Player.Balance += 0 # Push
            elif stand_hand.value > dealer_hand.value:
                stand_hand.Player.Balance += stand_hand.Bet
            else:
                stand_hand.Player.Balance -= stand_hand.Bet
        print stand_hand


def any_stand_hands():
    stand_hands = [hand for hand in finished_hands if hand.Status == State.Stand]
    return len(stand_hands) > 0


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
            play_hand(playing_hand, raw_input("(S)tand\(H)it\(D)ouble: "))

        finished_hands.append(playing_hand)

    # Show dealers' hand
    dealer_hand.Cards[0].flip()
    print
    print dealer_hand

    while dealer_hand.Status == State.Active and any_stand_hands():
        while dealer_hand.value < 16:
            raw_input("Hit any key to deal next card...")
            play_hand(dealer_hand, 'H')
        if dealer_hand.Status == State.Active:
            dealer_hand.Status = State.Stand
        print
        print dealer_hand

    # Pay
    pay_players()

    # Bankrupt everybody
    for player in active_players:
        # player.Balance -= player.Balance

    # Check remaining cash
    bankrupt_players = [player for player in active_players if player.Balance <= 0]
    active_players = [player for player in active_players if player.Balance > 0]

    print
    for player in bankrupt_players:
        print player.Name + " is bankrupt!"
    raw_input("Hit any key for the next round...")

print "Game over! House always wins!"
