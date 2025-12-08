class Product:
    _next_id = 1

    def __init__(self,
                 name: str,
                 purchase_price: float,
                 sell_price: float,
                 space: float):

        self.id = Product._next_id
        Product._next_id += 1
        self.name = name
        self.purchase_price = purchase_price
        self.sell_price = sell_price
        self.space = space

    def margin(self) -> float:
        return float(self.sell_price - self.purchase_price)

    def margin_percentage(self) -> float:
        return float((self.sell_price - self.purchase_price)
                     / self.purchase_price)

    def sell_value_for(self, quantity: int) -> float:
        return self.sell_price * quantity

    def purchase_cost_for(self, quantity: int) -> float:
        return self.purchase_price * quantity

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.id == other.id
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.id)
