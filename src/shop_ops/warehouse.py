from src.shop_ops.stock_item import StockItem
from src.shop_ops.product import Product


class Warehouse:
    def __init__(self, capacity: float) -> None:
        self._items: list[StockItem] = []
        self._capacity: float = capacity

    def get_quantity(self, product: Product) -> int:
        for item in self._items:
            if item.product == product:
                return item.quantity
        return 0

    def add_stock(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be > 0')

        for item in self._items:
            if item.product == product:
                item.quantity += quantity
                return

        item = StockItem(product=product, quantity=quantity)
        self._items.append(item)

    def remove_stock(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be > 0')

        for item in self._items:
            if item.product == product:
                if item.quantity < quantity:
                    raise ValueError('Not enough stock')
                item.quantity -= quantity
                return

        raise ValueError('Product not found in Warehouse')

    def get_used_space(self) -> float:
        used_space = 0
        for item in self._items:
            used_space += item.product.space * item.quantity
        return used_space
    # return sum(item.product.space * item.quantity for item in self._items)

    def get_available_space(self) -> float:
        return self._capacity - self.get_used_space()
