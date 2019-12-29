import unittest

from deck import Card
from hand import HandType, Hand, State
from player import Player


CARDS = {
    'Four': Card('4', 'S'),
    'Six': Card('6', 'H'),
    'Seven': Card('7', 'D'),
    'Jack': Card('J', 'D'),
    'Queen': Card('Q', 'C'),
    'King':Card('K', 'D'),
    'AceOfClubs': Card('A', 'C'),
    'AceOfSpades': Card('A', 'S'),
}


class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = Hand(Player("Player", 50), 10, HandType.PLAYER)
        self.dealer = Hand(Player("Dealer", None), 10, HandType.DEALER)

    def tearDown(self):
        self.hand.reset()
        self.dealer.reset()

    def test_value_numeric_numeric(self):
        self.hand.deal(CARDS['Four'])
        self.hand.deal(CARDS['Seven'])
        self.assertEqual(11, self.hand.value)

    def test_value_numeric_face(self):
        self.hand.deal(CARDS['Four'])
        self.hand.deal(CARDS['Jack'])
        self.assertEqual(14, self.hand.value)

    def test_value_face_ace(self):
        self.hand.deal(CARDS['Queen'])
        self.hand.deal(CARDS['AceOfSpades'])
        self.assertEqual(21, self.hand.value)

    def test_value_face_face(self):
        self.hand.deal(CARDS['Queen'])
        self.hand.deal(CARDS['King'])
        self.assertEqual(20, self.hand.value)

    def test_value_ace_ace(self):
        self.hand.deal(CARDS['AceOfClubs'])
        self.hand.deal(CARDS['AceOfSpades'])
        self.assertEqual(12, self.hand.value)

    def test_status_blackjack(self):
        self.hand.deal(CARDS['Queen'])
        self.hand.deal(CARDS['AceOfClubs'])
        self.assertEqual(State.BlackJack, self.hand.status)

    def test_status_bust(self):
        self.hand.deal(CARDS['Queen'])
        self.hand.deal(CARDS['Six'])
        self.hand.deal(CARDS['Seven'])
        self.assertEqual(State.Bust, self.hand.status)

    def test_status_can_split(self):
        self.hand.deal(CARDS['Queen'])
        self.hand.deal(CARDS['King'])
        self.assertEqual(True, self.hand.can_split)

    def test_balance_lose(self):
        self.hand.deal(CARDS['Four'])
        self.hand.deal(CARDS['Seven'])
        self.dealer.deal(CARDS['Queen'])
        self.dealer.deal(CARDS['King'])
        self.hand.game_value(self.dealer.value)
        self.assertEqual(40, self.hand.player.balance)

    def test_balance_win(self):
        self.hand.deal(CARDS['Jack'])
        self.hand.deal(CARDS['Six'])
        self.dealer.deal(CARDS['Four'])
        self.dealer.deal(CARDS['Seven'])
        self.hand.game_value(self.dealer.value)
        self.assertEqual(60, self.hand.player.balance)

    def test_balance_push(self):
        self.hand.deal(CARDS['AceOfClubs'])
        self.hand.deal(CARDS['Seven'])
        self.dealer.deal(CARDS['AceOfSpades'])
        self.dealer.deal(CARDS['Seven'])
        self.hand.game_value(self.dealer.value)
        self.assertEqual(50, self.hand.player.balance)


if __name__ == '__main__':
    unittest.main()
