import pytest

from src.shop_ops.product import Product
from src.shop_ops.warehouse import Warehouse
from src.shop_ops.shop import Shop
from src.shop_ops.supplier_order_line import SupplierOrderLine
from src.shop_ops.supplier_order import SupplierOrder, SupplierOrderStatus
from src.shop_ops.supplier_fulfillment_simulation import SupplierFulfillmentSimulation


@pytest.fixture
def product_milk() -> Product:
    return Product(
        name="Mleko",
        purchase_price=10,
        sell_price=15,
        space=1.0,
    )


@pytest.fixture
def warehouse() -> Warehouse:
    return Warehouse(capacity=100.0)


@pytest.fixture
def shop(warehouse: Warehouse) -> Shop:
    return Shop(warehouse=warehouse, budget=1000.0)


class TestSupplierFulfillmentSimulation:
    def test_run_for_day_delivers_only_orders_for_that_day(self,
                                                           shop,
                                                           product_milk):

        line_day2 = SupplierOrderLine(product_milk, 3)
        line_day3 = SupplierOrderLine(product_milk, 5)

        order_day2 = SupplierOrder([line_day2], delivery_day=2)
        order_day3 = SupplierOrder([line_day3], delivery_day=3)

        assert shop.warehouse.get_quantity(product_milk) == 0

        simulation = SupplierFulfillmentSimulation(
            [order_day2, order_day3]
        )

        delivered_today = simulation.run_for_day(shop, current_day=2)

        assert shop.warehouse.get_quantity(product_milk) == 3
        assert order_day2.status == SupplierOrderStatus.DELIVERED
        assert order_day3.status == SupplierOrderStatus.ORDERED

        assert delivered_today == [order_day2]

    def test_run_for_day_ignores_already_delivered_orders(self,
                                                          shop,
                                                          product_milk):
        line = SupplierOrderLine(product_milk, 4)

        order_already_delivered = SupplierOrder([line], delivery_day=2)
        order_already_delivered.status = SupplierOrderStatus.DELIVERED

        simulation = SupplierFulfillmentSimulation([order_already_delivered])

        assert shop.warehouse.get_quantity(product_milk) == 0

        delivered_today = simulation.run_for_day(shop, current_day=2)

        assert shop.warehouse.get_quantity(product_milk) == 0
        assert order_already_delivered.status == SupplierOrderStatus.DELIVERED
        assert delivered_today == []

    def test_for_day_with_no_orders_for_that_day_does_nothing(self,
                                                              shop,
                                                              product_milk):
        line = SupplierOrderLine(product_milk, 2)
        order_day5 = SupplierOrder([line], delivery_day=5)

        simulation = SupplierFulfillmentSimulation([order_day5])

        delivered_today = simulation.run_for_day(shop, current_day=3)

        assert delivered_today == []
        assert shop.warehouse.get_quantity(product_milk) == 0
        assert order_day5.status == SupplierOrderStatus.ORDERED

    def test_run_for_day_accepts_empty_order_list(self, shop):
        simulation = SupplierFulfillmentSimulation([])

        delivered_today = simulation.run_for_day(shop, current_day=1)

        assert delivered_today == []

    def test_run_for_day_validates_current_day_type(self, shop, product_milk):
        line = SupplierOrderLine(product_milk, 1)
        order = SupplierOrder([line], delivery_day=1)
        simulation = SupplierFulfillmentSimulation([order])

        with pytest.raises(ValueError):
            simulation.run_for_day(shop, current_day="1")

    def test_run_for_day_validates_current_day_non_negative(self,
                                                            shop,
                                                            product_milk):
        line = SupplierOrderLine(product_milk, 1)
        order = SupplierOrder([line], delivery_day=0)
        simulation = SupplierFulfillmentSimulation([order])

        with pytest.raises(ValueError):
            simulation.run_for_day(shop, current_day=-1)
