class Item:
    def __init__(self, profit, weight):
        self.profit = profit
        self.weight = weight

    def __str__(self):
        return "[profit {}, weight {}]".format(self.profit, self.weight)
