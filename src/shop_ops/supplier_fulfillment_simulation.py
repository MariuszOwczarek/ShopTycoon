from typing import Iterable
from src.shop_ops.shop import Shop
from src.shop_ops.supplier_order import SupplierOrder, SupplierOrderStatus


class SupplierFulfillmentSimulation:
    def __init__(self, supplier_orders: Iterable[SupplierOrder]) -> None:
        self.supplier_orders = list(supplier_orders)

    def run_for_day(self, shop: Shop, current_day: int) -> list[SupplierOrder]:
        if not isinstance(current_day, int):
            raise ValueError('current_day must an Integer')

        if current_day < 0:
            raise ValueError('delivery_day must be non-negative')

        delivered_today = []
        for supplier_order in self.supplier_orders:
            if (supplier_order.status == SupplierOrderStatus.ORDERED and
                    supplier_order.delivery_day == current_day):
                supplier_order.deliver(shop)
                delivered_today.append(supplier_order)
        return delivered_today
