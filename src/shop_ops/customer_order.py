from enum import Enum
from src.shop_ops.product import Product
from src.shop_ops.warehouse import Warehouse


class CustomerOrderStatus(Enum):
    PENDING = 1
    FULFILLED = 2
    REJECTED = 3


class CustomerOrder:
    _next_id = 1

    def __init__(self,
                 product: Product,
                 quantity: int,
                 status: CustomerOrderStatus = CustomerOrderStatus.PENDING):

        self.id = CustomerOrder._next_id
        CustomerOrder._next_id += 1
        self.product = product

        if quantity <= 0:
            raise ValueError("Quantity must be > 0")
        self.quantity: int = quantity
        self.status: CustomerOrderStatus = status

    def total_order_value(self) -> float:
        return self.product.sell_price * self.quantity

    def can_be_fulfilled(self, warehouse: Warehouse) -> bool:
        quantity_available = warehouse.get_quantity(self.product)
        if quantity_available >= self.quantity:
            return True
        return False

    def fulfill_order(self, warehouse: Warehouse) -> float:
        if self.can_be_fulfilled(warehouse):
            warehouse.remove_stock(self.product, self.quantity)
            order_value = self.total_order_value()
            self.status = CustomerOrderStatus.FULFILLED
            return order_value
        raise ValueError('Order cannot be filfilled')

    def reject_order(self) -> None:
        self.status = CustomerOrderStatus.REJECTED
