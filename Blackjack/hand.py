from enum import Enum
from colorama import Fore, Style
from pretty_printing import pretty_print


class State(Enum):
    Active = "Active"
    BlackJack = "BlackJack"
    Bust = "Bust"
    Stand = "Stand"


class HandType(Enum):
    PLAYER = 1
    DEALER = 2


TypeToColor = {
    HandType.PLAYER: Fore.LIGHTMAGENTA_EX,
    HandType.DEALER: Fore.LIGHTBLUE_EX,
}


class Hand(object):
    def __init__(self, current_player, bet, hand_type=HandType.PLAYER):
        """
        :param hand_type: HandType
        :param current_player: Player
        """
        self.Player = current_player
        self.Bet = bet
        self.Status = State.Active
        self.Cards = []
        self.CanSplit = False
        self.Type = hand_type

    @property
    def value(self):
        return len(self)

    def __str__(self):
        return TypeToColor[self.Type] + \
               str(self.Player.Name) + self.print_bet() + ':\t' + \
               ''.join(map(str, self.Cards)) + \
               '\tValue: ' + str(self.value) + ", " + \
               self.status_str() + \
               Style.RESET_ALL

    def __len__(self):
        value = 0
        for card in self.Cards:
            if not card.IsFaceDown:
                value += card.value
            if value > 21 and card.Rank == 'A':  # 'A' can be 1 or 11
                value -= 10
        return value

    def game_value(self, dealer_hand_value):
        """
        :params dealer_hand_value: Int
        """
        if self.value == dealer_hand_value:
            pretty_print(f"{self.Player.Name} - Push! No Winner.", Fore.LIGHTGREEN_EX)
            pass  # Push
        elif self.value > dealer_hand_value:
            pretty_print(f"{self.Player.Name} wins!", Fore.LIGHTGREEN_EX)
            self.Player.Balance += self.Bet
        else:
            pretty_print(f"{self.Player.Name} lost!", Fore.LIGHTRED_EX)
            self.Player.Balance -= self.Bet

    def deal(self, card):
        """
        :type card: Card
        """
        self.Cards.append(card)
        if self.value == 21 and len(self.Cards) == 2:
            self.Status = State.BlackJack
        if self.value > 21:
            self.Status = State.Bust
        if len(self.Cards) == 2 and \
                self.Cards[0].value == self.Cards[1].value:
            self.CanSplit = True

    def reset(self):
        self.Status = State.Active
        self.Cards = []
        self.CanSplit = False

    def print_status(self):
        player_name = self.Player.Name
        print(self)
        if self.value == 21:
            pretty_print(f"21! {player_name}, your'e done", Fore.LIGHTGREEN_EX)
            self.Status = State.Stand
        elif self.Status == State.Bust:
            pretty_print(f"{str(self.value)}. Your hand is dead, {player_name}", Fore.LIGHTRED_EX)

    def print(self, dealer_hand):
        """
        :param dealer_hand: Hand
        """
        print()
        print(dealer_hand)
        print(self)
        print(f"{self.Player.Name}, what do you do?")

    def print_bet(self):
        if self.Type == HandType.DEALER:
            return ""
        return ',' + str(self.Bet)

    def status_str(self):
        for card in self.Cards:
            if card.IsFaceDown:
                return '???'
        return str(self.Status)
