from enum import Enum


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
               ", " + self.Status

    def __len__(self):
        value = 0
        for card in self.Cards:
            if not card.IsFaceDown:
                value += card.value
            if value > 21 and card.Rank == 'A':
                # 'A' can be 1 or 11
                value -= 10
        return value

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
