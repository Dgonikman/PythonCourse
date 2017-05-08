from enum import Enum


class State(Enum):
    Active = "Active"
    BlackJack = "BlackJack"
    Bust = "Bust"
    Stand = "Stand"


def value_of(rank):
    """
    :param rank: Card rank 
    :return: integer value of the rank
    """
    return \
    {
        'A': 11,
        'K': 10,
        'Q': 10,
        'J': 10,
        '10': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
    }.get(rank, 0)


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
        return str(self.Player.Name) + ',' + str(self.Bet) + ':\t' + \
               ''.join(map(str, self.Cards)) + '\tValue: ' + str(self.value) + \
               ", " + self.Status

    def __len__(self):
        value = 0
        for card in self.Cards:
            if not card.IsFaceDown:
                value += value_of(card.Rank)
            if value > 21 and card.Rank == 'A':
                # 'A' can be 1 or 11
                value -= 10
        return value

    def deal(self, card):
        self.Cards.append(card)
        if self.value == 21 and len(self.Cards) == 2:
            self.Status = State.BlackJack
        if self.value > 21:
            self.Status = State.Bust

    def reset(self):
        self.Status = State.Active
        self.Cards = []
