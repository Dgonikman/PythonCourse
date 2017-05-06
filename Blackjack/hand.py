from enum import Enum


class State(Enum):
    Active = 0
    Bust = 1
    Stand = 2


class Hand(object):
    def __init__(self, current_player, bet):
        self.Player = current_player
        self.Bet = bet
        self.Status = State.Active
        self.Cards = []

    @property
    def value(self):
        return len(self)

    def __str__(self):
        return str(self.Player.Name) + ',' + str(self.Bet) + ':' + \
               ''.join(map(str, self.Cards)) + ' Value: ' + str(self.value)

    def __len__(self):
        # TODO: should be value of the cards
        return len(self.Cards)

    def deal(self, card):
        self.Cards.append(card)
        if self.value > 21:
            self.Status = State.Bust
