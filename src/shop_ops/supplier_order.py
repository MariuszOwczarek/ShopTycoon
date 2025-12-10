from typing import Iterable
from src.shop_ops.supplier_order_line import SupplierOrderLine
from src.shop_ops.shop import Shop
from enum import Enum


class SupplierOrderStatus(Enum):
    ORDERED = 1
    DELIVERED = 2


class SupplierOrder:
    def __init__(self, lines: Iterable[SupplierOrderLine], delivery_day: int):

        lines_list = list(lines)
        if not lines_list:
            raise ValueError('Supplier order must have at least one line')

        for line in lines_list:
            if not isinstance(line, SupplierOrderLine):
                raise ValueError("All lines must be SupplierOrderLine"
                                 " instances")

        if not isinstance(delivery_day, int):
            raise ValueError("Delivery day must be an integer")

        if delivery_day < 0:
            raise ValueError("Delivery day must be non-negative")

        self.lines: list[SupplierOrderLine] = lines_list
        self.status = SupplierOrderStatus.ORDERED
        self.delivery_day = delivery_day

    def total_cost(self) -> float:
        return sum(line.line_cost() for line in self.lines)

    def deliver(self, shop: Shop) -> None:

        if self.status != SupplierOrderStatus.ORDERED:
            raise ValueError("Supplier order cannot be delivered"
                             " in its current status")

        for line in self.lines:
            shop.warehouse.add_stock(line.product, line.quantity)
        self.status = SupplierOrderStatus.DELIVERED
