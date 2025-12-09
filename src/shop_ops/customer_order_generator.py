from src.shop_ops.product import Product
from src.shop_ops.customer_order import CustomerOrder, CustomerOrderStatus
import random


class CustomerOrderGenerator:
    def __init__(self,
                 min_orders_per_day: int,
                 max_orders_per_day: int,
                 min_quantity_per_order: int,
                 max_quantity_per_order: int,
                 seed=123):

        if min_orders_per_day <= 0:
            raise ValueError('Minimum Quantity must be > 0')

        if max_orders_per_day <= min_orders_per_day:
            raise ValueError('Maximum Orders Number must be '
                             '> Minimum Orders Number')

        if min_quantity_per_order <= 0:
            raise ValueError('Minimum Quantity must be > 0')

        if max_quantity_per_order < min_quantity_per_order:
            raise ValueError('Maximum Quantity must be > Minimum Quantity')

        self.min_orders_per_day: int = min_orders_per_day
        self.max_orders_per_day: int = max_orders_per_day
        self.min_quantity_per_order: int = min_quantity_per_order
        self.max_quantity_per_order: int = max_quantity_per_order
        self._rng = random.Random(seed)

    def generate_orders(self, products: list[Product]) -> list[CustomerOrder]:
        if len(products) == 0:
            raise ValueError('Products list must not be empty')

        order_list: list[CustomerOrder] = []
        n = self._rng.randrange(self.min_orders_per_day,
                                self.max_orders_per_day + 1)

        for _ in range(n):
            product = products[self._rng.randint(0, len(products) - 1)]
            quantity = self._rng.randrange(
                self.min_quantity_per_order,
                self.max_quantity_per_order + 1)
            order_list.append(
                CustomerOrder(product=product,
                              quantity=quantity,
                              status=CustomerOrderStatus.PENDING))
        return order_list
