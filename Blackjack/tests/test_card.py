import unittest

from deck import Card


class TestCard(unittest.TestCase):
    def test_len_1(self):
        my_card = Card('A', 'D')
        self.assertEqual(11, len(my_card))

    def test_len_2(self):
        my_card = Card('Q', 'D')
        self.assertEqual(10, len(my_card))

    def test_len_3(self):
        my_card = Card('4', 'D')
        self.assertEqual(4, len(my_card))


if __name__ == '__main__':
    unittest.main()
