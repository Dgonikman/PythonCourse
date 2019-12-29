from enum import Enum
from colorama import Fore
from pretty_printing import pretty_print


class State(Enum):
    Active = "Active"
    BlackJack = "BlackJack"
    Bust = "Bust"
    Stand = "Stand"


class Hand(object):
    def __init__(self, current_player, bet):
        self.Player = current_player
        self.Bet = bet
        self.Status = State.Active
        self.Cards = []
        self.CanSplit = False

    @property
    def value(self):
        return len(self)

    def __str__(self):
        return str(self.Player.Name) + ',' + str(self.Bet) + ':\t' + \
               ''.join(map(str, self.Cards)) + '\tValue: ' + str(self.value) + \
               ", " + str(self.Status)

    def __len__(self):
        value = 0
        for card in self.Cards:
            if not card.IsFaceDown:
                value += card.value
            if value > 21 and card.Rank == 'A':
                # 'A' can be 1 or 11
                value -= 10
        return value

    def game_value(self, dealer_hand_value):
        """
        :params dealer_hand_value: Int
        """
        if self.value == dealer_hand_value:
            pretty_print(f"{self.Player.Name} - Push! No Winner.", Fore.LIGHTGREEN_EX)
            pass # Push
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
        if self.Status == State.BlackJack:
            print(f"21! {player_name}, your'e done")
            self.Status = State.Stand
        elif self.Status == State.Bust:
            print(f"{str(self.value)}. Your hand is dead, {player_name}")

    def print(self, dealer_hand):
        """
        :param dealer_hand: Hand
        """
        print()
        print(dealer_hand)
        print(self)
        print(f"{self.Player.Name}, what do you do?")
