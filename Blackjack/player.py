"""
Blackjack player module
"""


class Player:
    """
    Player class
    """
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def __len__(self):
        return self.balance

    def __str__(self):
        return f"{self.name}: {self.balance}$"
