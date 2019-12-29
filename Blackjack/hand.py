"""
BlackJack hand module
"""
from enum import Enum
from colorama import Fore, Style
from pretty_printing import pretty_print


class State(Enum):
    """
    Enum for hand activity state
    """
    Active = "Active"
    BlackJack = "BlackJack"
    Bust = "Bust"
    Stand = "Stand"


class HandType(Enum):
    """
    Enum for player type
    """
    PLAYER = 1
    DEALER = 2


TYPE_TO_COLOR = {
    HandType.PLAYER: Fore.LIGHTMAGENTA_EX,
    HandType.DEALER: Fore.LIGHTBLUE_EX,
}


class Hand:
    """
    Class representation of a blackjack hand
    """
    def __init__(self, current_player, bet, hand_type=HandType.PLAYER):
        """
        :type hand_type: HandType
        :type current_player: Player
        """
        self.player = current_player
        self.bet = bet
        self.status = State.Active
        self.cards = []
        self.can_split = False
        self.type = hand_type

    @property
    def value(self):
        """
        :return: Integer value of the hand
        :rtype: int
        """
        return len(self)

    def __str__(self):
        return TYPE_TO_COLOR[self.type] + \
               str(self.player.name) + self.print_bet() + ':\t' + \
               ''.join(map(str, self.cards)) + \
               '\tValue: ' + str(self.value) + ", " + \
               self.status_str() + \
               Style.RESET_ALL

    def __len__(self):
        value = 0
        for card in self.cards:
            if not card.is_face_down:
                value += card.value
            if value > 21 and card.rank == 'A':  # 'A' can be 1 or 11
                value -= 10
        return value

    def game_value(self, dealer_hand_value):
        """
        :type dealer_hand_value: int
        """
        if self.value == dealer_hand_value:  # Push
            pretty_print(f"{self.player.name} - Push! No Winner.", Fore.LIGHTGREEN_EX)
        elif self.value > dealer_hand_value:
            pretty_print(f"{self.player.name} wins!", Fore.LIGHTGREEN_EX)
            self.player.balance += self.bet
        else:
            pretty_print(f"{self.player.name} lost!", Fore.LIGHTRED_EX)
            self.player.balance -= self.bet

    def deal(self, card):
        """
        :type card: Card
        """
        self.cards.append(card)
        if self.value == 21 and len(self.cards) == 2:
            self.status = State.BlackJack
        if self.value > 21:
            self.status = State.Bust
        if len(self.cards) == 2 and \
                self.cards[0].value == self.cards[1].value:
            self.can_split = True

    def reset(self):
        """
        Reset hand.
        """
        self.status = State.Active
        self.cards = []
        self.can_split = False

    def print_status(self):
        """
        Prints hand status.
        """
        player_name = self.player.name
        print(self)
        if self.value == 21:
            pretty_print(f"21! {player_name}, your'e done", Fore.LIGHTGREEN_EX)
            self.status = State.Stand
        elif self.status == State.Bust:
            pretty_print(f"{str(self.value)}. Your hand is dead, {player_name}", Fore.LIGHTRED_EX)

    def print(self, dealer_hand):
        """
        :type dealer_hand: Hand
        """
        print()
        print(dealer_hand)
        print(self)
        print(f"{self.player.name}, what do you do?")

    def print_bet(self):
        """
        Displays bet for players only.
        """
        if self.type == HandType.DEALER:
            return ""
        return ',' + str(self.bet)

    def status_str(self):
        """
        :return: String representation of status. Hidden if a card is face down.
        """
        for card in self.cards:
            if card.is_face_down:
                return '???'
        return str(self.status)
