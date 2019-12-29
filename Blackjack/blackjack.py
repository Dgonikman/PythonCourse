"""
BlackJack game - main class.
"""

from colorama import Fore
from deck import Shoe
from player import Player
from hand import Hand, State, HandType
from pretty_printing import pretty_print_lose, pretty_print_win, pretty_input, pretty_print_error, pretty_print_info


def play_hand(hand_to_play, action):
    """
    :param action: players' move
    :type hand_to_play: Hand
    """
    player_name = hand_to_play.player.name
    if action in ('S', 's'):
        pretty_print_info(f"{player_name} chose to stand")
        hand_to_play.status = State.Stand
    elif action in ('H', 'h'):
        pretty_print_info(f"{player_name} chose to hit")
        hand_to_play.deal(shoe.pop())
    elif action in ('D', 'd'):
        pretty_print_info(f"{player_name} chose to double")
        hand_to_play.bet *= 2
        hand_to_play.deal(shoe.pop())
        if hand_to_play.value < 21:
            hand_to_play.status = State.Stand
    elif action in ('P', 'p'):
        first_hand = split_hand(hand_to_play, 0)
        second_hand = split_hand(hand_to_play, 1)
        return first_hand, second_hand
    else:
        pretty_print_error("Illegal move, try again.")
    return hand_to_play, None


def split_hand(hand_to_play, idx):
    """
    :param idx: card index in hand
    :type hand_to_play: Hand
    """
    new_hand = Hand(hand_to_play.player, hand_to_play.bet, HandType.PLAYER)
    new_hand.deal(hand_to_play.cards[idx])
    new_hand.deal(shoe.pop())
    return new_hand


def pay_players():
    """
    Evaluate players' hands against dealer.
    """
    blackjack_hands = filter(lambda h: h.status == State.BlackJack, finished_hands)
    bust_hands = filter(lambda h: h.status == State.Bust, finished_hands)
    stand_hands = filter(lambda h: h.status == State.Stand, finished_hands)

    for bust_hand in bust_hands:
        bust_hand.player.balance -= bust_hand.bet
        pretty_print_lose(f"{bust_hand.player.name} is bust!")
        print(bust_hand)

    for blackjack_hand in blackjack_hands:
        blackjack_hand.player.balance += 1.5 * blackjack_hand.bet
        pretty_print_win(f"{blackjack_hand.player.name}, BLACKJACK!")
        print(blackjack_hand)

    for stand_hand in stand_hands:
        if dealer_hand.status == State.Bust:
            pretty_print_win(f"Dealer is Bust! {stand_hand.player.name} wins!")
            stand_hand.player.balance += stand_hand.bet
        else:  # Dealer Stand or Blackjack
            stand_hand.game_value(dealer_hand.value)
        print(stand_hand)


def any_stand_hands():
    """
    :return: Has any hands in Stand state
    """
    stand_hands = [h for h in finished_hands if h.status == State.Stand]
    return len(stand_hands) > 0


# Pretty printing
def break_line():
    """
    Print line break
    """
    breaker = ''
    for _ in range(0, 60):
        breaker += '-'
    print(breaker)


def tab_offset():
    """
    Offset output text
    """
    offset = ''
    for _ in range(0, 8):
        offset += '\t'
    return offset


# Constants
INITIAL_BALANCE = 100
MINIMAL_BET = 10

# Globals
dealer_hand = Hand(Player("Dealer", None), None, HandType.DEALER)
active_players = [Player("Player1", INITIAL_BALANCE)]
shoe = Shoe(6)
rounds = 0

# Game
if __name__ == '__main__':
    while len(active_players) > 0:
        # Init round
        rounds += 1
        active_hands = []
        finished_hands = []
        dealer_hand.reset()
        break_line()
        for player in active_players:
            active_hands.append(Hand(player, MINIMAL_BET, HandType.PLAYER))
        print(f"Round #{rounds}")

        # Deal hands
        for _ in range(0, 2):
            for hand in active_hands:
                hand.deal(shoe.pop())
            dealer_hand.deal(shoe.pop())
        dealer_hand.cards[0].flip()

        # Print hands
        print()
        print(dealer_hand)
        for hand in active_hands:
            print(hand)
        break_line()

        # Gameplay
        while len(active_hands) > 0:
            playing_hand = active_hands.pop(0)
            while playing_hand.status == State.Active:
                playing_hand.print(dealer_hand)
                possible_actions = "(S)tand\\(H)it\\(D)ouble"
                if playing_hand.can_split:
                    possible_actions += "\\s(P)lit"
                hand1, hand2 = play_hand(playing_hand, pretty_input(possible_actions + ": "))
                playing_hand = hand1
                if hand2 is not None:
                    active_hands.insert(0, hand2)
                playing_hand.print_status()
            finished_hands.append(playing_hand)
            break_line()

        # Show dealers' hand
        dealer_hand.cards[0].flip()
        print()
        print(dealer_hand)

        while dealer_hand.status == State.Active and any_stand_hands():
            while dealer_hand.value < 16:
                pretty_input("Hit any key to deal next card...")
                play_hand(dealer_hand, 'H')
                dealer_hand.print_status()
            if dealer_hand.status == State.Active:
                dealer_hand.status = State.Stand
            print()
            print(dealer_hand)

        # Pay
        pay_players()

        # Bankrupt everybody
        for player in active_players:
            pretty_print_info(tab_offset() + str(player))
            # player.balance -= player.balance

        # Check remaining cash
        bankrupt_players = [p for p in active_players if p.balance <= 0]
        active_players = [p for p in active_players if p.balance > 0]

        print()
        for player in bankrupt_players:
            pretty_print_lose(f"{player.name} is bankrupt!")
        pretty_input("Hit any key for the next round...", Fore.YELLOW)

    print("Game over! House always wins!")
