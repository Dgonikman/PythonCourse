from deck import Shoe
from player import Player
from hand import Hand, State


def play_hand(hand_to_play, action):
    """
    :param action: players' move
    :type hand_to_play: Hand
    """
    player_name = hand_to_play.Player.Name
    if action == 'S' or action == 's':
        print(f"{player_name } chose to stand")
        hand_to_play.Status = State.Stand
    elif action == 'H' or action == 'h':
        print(f"{player_name } chose to hit")
        hand_to_play.deal(shoe.pop())
    elif action == 'D' or action == 'd':
        print(f"{player_name } chose to double")
        hand_to_play.Bet *= 2
        hand_to_play.deal(shoe.pop())
        if hand_to_play.value < 21:
            hand_to_play.Status = State.Stand
    elif action == 'P' or action == 'p':
        first_hand = split_hand(hand_to_play, 0)
        second_hand = split_hand(hand_to_play, 1)
        return first_hand, second_hand
    else:
        print("Illegal move, try again.")
    return hand_to_play, None


def split_hand(hand_to_play, idx):
    """
    :param idx: card index in hand
    :type hand_to_play: Hand
    """
    new_hand = Hand(hand_to_play.Player, hand_to_play.Bet)
    new_hand.deal(hand_to_play.Cards[idx])
    new_hand.deal(shoe.pop())
    return new_hand


def pay_players():
    blackjack_hands = filter(lambda h: h.Status == State.BlackJack, finished_hands)
    bust_hands = filter(lambda h: h.Status == State.Bust, finished_hands)
    stand_hands = filter(lambda h: h.Status == State.Stand, finished_hands)

    for bust_hand in bust_hands:
        bust_hand.Player.Balance -= bust_hand.Bet
        print(bust_hand)

    for blackjack_hand in blackjack_hands:
        blackjack_hand.Player.Balance += 1.5 * blackjack_hand.Bet
        print(blackjack_hand)

    for stand_hand in stand_hands:
        if dealer_hand.Status == State.Bust:
            stand_hand.Player.Balance += stand_hand.Bet
        else:  # Dealer Stand or Blackjack
            if stand_hand.value == dealer_hand.value:
                stand_hand.Player.Balance += 0  # Push
            elif stand_hand.value > dealer_hand.value:
                stand_hand.Player.Balance += stand_hand.Bet
            else:
                stand_hand.Player.Balance -= stand_hand.Bet
        print(stand_hand)


def any_stand_hands():
    stand_hands = [h for h in finished_hands if h.Status == State.Stand]
    return len(stand_hands) > 0


# Pretty printing
def print_hand(hand_to_print):
    """
    :type hand_to_print: Hand
    """
    print()
    print(dealer_hand)
    print(hand_to_print)
    print(f"{hand_to_print.Player.Name}, what do you do?")


def print_hand_status(hand_to_print):
    """
    :type hand_to_print: Hand
    """
    player_name = hand_to_print.Player.Name
    print(hand_to_print)
    if hand_to_print.Status == State.BlackJack:
        print(f"21! {player_name}, your'e done")
        hand_to_print.Status = State.Stand
    elif hand_to_print.Status == State.Bust:
        print(f"{str(hand_to_print.value)}. Your hand is dead, {player_name}")


def break_line():
    breaker = ''
    for _ in range(0, 60):
        breaker += '-'
    print(breaker)


def tab_offset():
    offset = ''
    for _ in range(0, 8):
        offset += '\t'
    return offset


# Constants
INITIAL_BALANCE = 100
MINIMAL_BET = 10

# Globals
dealer_hand = Hand(Player("Dealer", None), None)
active_players = [Player("Player1", INITIAL_BALANCE)]
shoe = Shoe(6)
rounds = 0

# Game
while len(active_players) > 0:
    # Init round
    rounds += 1
    active_hands = []
    finished_hands = []
    dealer_hand.reset()
    break_line()
    for player in active_players:
        active_hands.append(Hand(player, MINIMAL_BET))
    print(f"Round #{rounds}")

    # Deal hands
    for _ in range(0, 2):
        for hand in active_hands:
            hand.deal(shoe.pop())
        dealer_hand.deal(shoe.pop())
    dealer_hand.Cards[0].flip()

    # Print hands
    print()
    print(dealer_hand)
    for hand in active_hands:
        print(hand)
    break_line()

    # Gameplay
    while len(active_hands) > 0:
        playing_hand = active_hands.pop(0)
        while playing_hand.Status == State.Active:
            print_hand(playing_hand)
            possible_actions = "(S)tand\(H)it\(D)ouble"
            if playing_hand.CanSplit:
                possible_actions += "\s(P)lit"
            hand1, hand2 = play_hand(playing_hand, input(possible_actions + ": "))
            playing_hand = hand1
            if hand2 is not None:
                active_hands.insert(0, hand2)
            print_hand_status(playing_hand)
        finished_hands.append(playing_hand)
        break_line()

    # Show dealers' hand
    dealer_hand.Cards[0].flip()
    print()
    print(dealer_hand)

    while dealer_hand.Status == State.Active and any_stand_hands():
        while dealer_hand.value < 16:
            input("Hit any key to deal next card...")
            play_hand(dealer_hand, 'H')
            print_hand_status(dealer_hand)
        if dealer_hand.Status == State.Active:
            dealer_hand.Status = State.Stand
        print()
        print(dealer_hand)

    # Pay
    pay_players()

    # Bankrupt everybody
    for player in active_players:
        print(tab_offset() + str(player))
        # player.Balance -= player.Balance

    # Check remaining cash
    bankrupt_players = [p for p in active_players if p.Balance <= 0]
    active_players = [p for p in active_players if p.Balance > 0]

    print()
    for player in bankrupt_players:
        print(f"{player.Name} is bankrupt!")
    input("Hit any key for the next round...")

print("Game over! House always wins!")
