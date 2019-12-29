class Player(object):
    def __init__(self, name, balance):
        self.Name = name
        self.Balance = balance

    def __len__(self):
        return self.Balance

    def __str__(self):
        return f"{self.Name}: {self.Balance}$"
