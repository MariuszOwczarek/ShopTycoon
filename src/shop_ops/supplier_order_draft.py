from src.shop_ops.shop import Shop
from src.shop_ops.product import Product
from src.shop_ops.supplier_order import SupplierOrder
from src.shop_ops.supplier_order_line import SupplierOrderLine


class SupplierOrderDraft:
    def __init__(self) -> None:
        self.lines: list[SupplierOrderLine] = []

    def add_line(self,
                 shop: Shop,
                 product: Product,
                 quantity: int) -> SupplierOrderLine:

        new_line = SupplierOrderLine(product, quantity)
        new_total_cost = self.total_cost() + new_line.line_cost()
        new_total_space = self.total_space() + product.space * quantity
        budget = shop.budget
        available_space = shop.warehouse.get_available_space()

        if new_total_space > available_space:
            raise ValueError("Not enough warehouse space for this line")

        if new_total_cost > budget:
            raise ValueError("Not enough budget for this line")

        self.lines.append(new_line)
        return new_line

    def total_cost(self) -> float:
        return sum(line.line_cost() for line in self.lines)

    def total_space(self) -> float:
        return sum(line.product.space * line.quantity for line in self.lines)

    def confirm(self, shop: Shop, delivery_day: int) -> SupplierOrder:
        if not self.lines:
            raise ValueError('Cannot confirm an empty supplier order draft')

        total_cost = self.total_cost()
        total_space = self.total_space()

        if total_cost > shop.budget:
            raise ValueError('Not enough budget to confirm supplier order')

        if total_space > shop.warehouse.get_available_space():
            raise ValueError('Not enough warehouse space to '
                             'confirm supplier order')

        supplier_order = SupplierOrder(self.lines, delivery_day)
        shop.budget -= total_cost
        return supplier_order
