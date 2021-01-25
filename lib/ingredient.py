class Ingredient:
    def __init__(self, name, quantity=0):
        self.name = name
        self.quantity = quantity

    def add(self, quantity=1):
        self.quantity = self.quantity + int(quantity)
