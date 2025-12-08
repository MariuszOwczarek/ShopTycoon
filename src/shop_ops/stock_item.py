from src.shop_ops.product import Product


class StockItem:
    _next_id = 1

    def __init__(self, product: Product, quantity: int):
        self.id = Product._next_id
        StockItem._next_id += 1
        self.product = product
        self.quantity: int = quantity

    def increase(self, inc_quantity: int) -> None:
        self.quantity += inc_quantity

    def decrease(self, dec_quantity: int) -> None:
        self.quantity -= dec_quantity

    def total_sell_value(self):
        return self.product.sell_value_for(self.quantity)

    def total_purchase_cost(self):
        return self.product.purchase_cost_for(self.quantity)
