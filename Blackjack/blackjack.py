from deck import Shoe
from player import Player
from hand import Hand, State
from pretty_printing import *


def play_hand(hand_to_play, action):
    """
    :param action: players' move
    :type hand_to_play: Hand
    """
    player_name = hand_to_play.Player.Name
    if action == 'S' or action == 's':
        pretty_print(f"{player_name} chose to stand", Fore.CYAN)
        hand_to_play.Status = State.Stand
    elif action == 'H' or action == 'h':
        pretty_print(f"{player_name} chose to hit", Fore.CYAN)
        hand_to_play.deal(shoe.pop())
    elif action == 'D' or action == 'd':
        pretty_print(f"{player_name} chose to double", Fore.CYAN)
        hand_to_play.Bet *= 2
        hand_to_play.deal(shoe.pop())
        if hand_to_play.value < 21:
            hand_to_play.Status = State.Stand
    elif action == 'P' or action == 'p':
        first_hand = split_hand(hand_to_play, 0)
        second_hand = split_hand(hand_to_play, 1)
        return first_hand, second_hand
    else:
        pretty_print("Illegal move, try again.", Fore.RED)
    return hand_to_play, None


def split_hand(hand_to_play, idx):
    """
    :param idx: card index in hand
    :type hand_to_play: Hand
    """
    new_hand = Hand(hand_to_play.Player, hand_to_play.Bet, Fore.LIGHTMAGENTA_EX)
    new_hand.deal(hand_to_play.Cards[idx])
    new_hand.deal(shoe.pop())
    return new_hand


def pay_players():
    blackjack_hands = filter(lambda h: h.Status == State.BlackJack, finished_hands)
    bust_hands = filter(lambda h: h.Status == State.Bust, finished_hands)
    stand_hands = filter(lambda h: h.Status == State.Stand, finished_hands)

    for bust_hand in bust_hands:
        bust_hand.Player.Balance -= bust_hand.Bet
        pretty_print(f"{bust_hand.Player.Name} is bust!", Fore.LIGHTRED_EX)
        print(bust_hand)

    for blackjack_hand in blackjack_hands:
        blackjack_hand.Player.Balance += 1.5 * blackjack_hand.Bet
        pretty_print(f"\t{blackjack_hand.Player.Name}, BLACKJACK!", Fore.LIGHTGREEN_EX)
        print(blackjack_hand)

    for stand_hand in stand_hands:
        if dealer_hand.Status == State.Bust:
            pretty_print(f"Dealer is Bust! {stand_hand.Player.Name} wins!", Fore.LIGHTGREEN_EX)
            stand_hand.Player.Balance += stand_hand.Bet
        else:  # Dealer Stand or Blackjack
            stand_hand.game_value(dealer_hand.value)
        print(stand_hand)


def any_stand_hands():
    stand_hands = [h for h in finished_hands if h.Status == State.Stand]
    return len(stand_hands) > 0


# Pretty printing
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
dealer_hand = Hand(Player("Dealer", None), None, Fore.LIGHTBLUE_EX)
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
            active_hands.append(Hand(player, MINIMAL_BET, Fore.LIGHTMAGENTA_EX))
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
                playing_hand.print(dealer_hand)
                possible_actions = "(S)tand\(H)it\(D)ouble"
                if playing_hand.CanSplit:
                    possible_actions += "\s(P)lit"
                hand1, hand2 = play_hand(playing_hand, pretty_input(possible_actions + ": "))
                playing_hand = hand1
                if hand2 is not None:
                    active_hands.insert(0, hand2)
                playing_hand.print_status()
            finished_hands.append(playing_hand)
            break_line()

        # Show dealers' hand
        dealer_hand.Cards[0].flip()
        print()
        print(dealer_hand)

        while dealer_hand.Status == State.Active and any_stand_hands():
            while dealer_hand.value < 16:
                pretty_input("Hit any key to deal next card...")
                play_hand(dealer_hand, 'H')
                dealer_hand.print_status()
            if dealer_hand.Status == State.Active:
                dealer_hand.Status = State.Stand
            print()
            print(dealer_hand)

        # Pay
        pay_players()

        # Bankrupt everybody
        for player in active_players:
            pretty_print(tab_offset() + str(player), Fore.CYAN)
            # player.Balance -= player.Balance

        # Check remaining cash
        bankrupt_players = [p for p in active_players if p.Balance <= 0]
        active_players = [p for p in active_players if p.Balance > 0]

        print()
        for player in bankrupt_players:
            pretty_print(f"{player.Name} is bankrupt!", Fore.LIGHTRED_EX)
        pretty_input("Hit any key for the next round...")

    print("Game over! House always wins!")
