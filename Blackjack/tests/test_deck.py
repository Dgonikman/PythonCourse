import unittest

from deck import Deck


class TestDeck(unittest.TestCase):
    def test_init(self):
        my_deck = Deck()
        self.assertEqual(52, len(my_deck))

    def test_pop(self):
        my_deck = Deck()
        my_deck.pop()
        self.assertEqual(51, len(my_deck))


if __name__ == '__main__':
    unittest.main()
