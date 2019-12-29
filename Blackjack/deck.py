"""
Playing Cards module
"""
import random

RANKS = ('A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2')
SUITS = ("Spades", "Clubs", "Hearts", "Diamonds")


class Card:
    """
    A class for a single card
    """
    def __init__(self, rank, suit, is_face_down=False):
        self.rank = rank
        self.suit = suit
        self.is_face_down = is_face_down

    def __str__(self):
        if self.is_face_down:
            return "(*,*)"
        return f"({self.rank},{self.suit[0]})"

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
            }.get(self.rank, 0)

    def flip(self):
        """
        :return: None
        """
        self.is_face_down = not self.is_face_down

    @property
    def value(self):
        """
        :return: integer value of a card
        :rtype: int
        """
        return len(self)


class Deck:
    """
    A class for a deck of cards
    """
    def __init__(self, init_shuffle=False):
        self.cards = []

        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(rank, suit))
        if init_shuffle:
            self.shuffle()

    def __len__(self):
        return len(self.cards)

    def pop(self):
        """
        :return: Card
        """
        top = self.cards[0]
        self.cards.remove(top)
        return top

    def shuffle(self):
        """
        Shuffle deck
        """
        random.shuffle(self.cards)


class Shoe:
    """
    A class for Casino shoe - multiple decks
    """
    def __init__(self, number_of_decks):
        self.number_of_decks = number_of_decks
        self.decks = []

        for _ in range(0, number_of_decks):
            self.decks.append(Deck(True))

    def __len__(self):
        return self.number_of_decks

    def pop(self):
        """
        :return: Card
        """
        deck_to_pop = random.randrange(0, self.number_of_decks)
        return self.decks[deck_to_pop].pop()
