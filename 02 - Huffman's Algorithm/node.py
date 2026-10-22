class Node:
    def __init__(self, probability, symbol='', left=None, right=None):
        self.left = left
        self.right = right
        self.probability = probability
        self.symbol = symbol