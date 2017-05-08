import random

RANKS = ('A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2')
SUITS = ("Spades", "Clubs", "Hearts", "Diamonds")


class Card(object):
    def __init__(self, rank, suit, is_face_down=False):
        self.Rank = rank
        self.Suit = suit
        self.IsFaceDown = is_face_down

    def __str__(self):
        if self.IsFaceDown:
            return "(*,*)"
        return "({r},{s})".format(r=self.Rank, s=self.Suit[0])

    def __len__(self):
        """
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
            }.get(self.Rank, 0)

    def flip(self):
        """
        :return: None 
        """
        self.IsFaceDown = not self.IsFaceDown

    @property
    def value(self):
        return len(self)


class Deck(object):
    def __init__(self, init_shuffle=False):
        self.Cards = []

        for suit in SUITS:
            for rank in RANKS:
                self.Cards.append(Card(rank, suit))
        if init_shuffle:
            self.shuffle()

    def __len__(self):
        return len(self.Cards)

    def pop(self):
        """
        :return: Card
        """
        top = self.Cards[0]
        self.Cards.remove(top)
        return top

    def shuffle(self):
        random.shuffle(self.Cards)


class Shoe(object):
    def __init__(self, number_of_decks):
        self.NumberOfDecks = number_of_decks
        self.Decks = []

        for _ in xrange(0, number_of_decks):
            self.Decks.append(Deck(True))

    def __len__(self):
        return self.NumberOfDecks

    def pop(self):
        """
        :return: Card
        """
        deck_to_pop = random.randrange(0, self.NumberOfDecks)
        return self.Decks[deck_to_pop].pop()
