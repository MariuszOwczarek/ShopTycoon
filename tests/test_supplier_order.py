import pytest
from src.shop_ops.supplier_order import SupplierOrder, SupplierOrderStatus
from src.shop_ops.supplier_order_line import SupplierOrderLine
from src.shop_ops.product import Product
from src.shop_ops.warehouse import Warehouse
from src.shop_ops.shop import Shop


@pytest.fixture
def product() -> Product:
    return Product(
        name="Mleko",
        purchase_price=10,
        sell_price=15,
        space=0.1,
    )


@pytest.fixture
def product2() -> Product:
    return Product(
        name="Chleb",
        purchase_price=15,
        sell_price=12,
        space=0.1,
    )


@pytest.fixture
def order_line(product) -> SupplierOrderLine:
    return SupplierOrderLine(product, 20)


class TestSupplierOrder:
    def test_supplier_order_initialization(self, order_line):
        supplier_order = SupplierOrder([order_line], 2)

        assert isinstance(supplier_order.lines, list)
        assert supplier_order.lines == [order_line]
        assert supplier_order.status == SupplierOrderStatus.ORDERED
        assert supplier_order.delivery_day == 2

    def test_empty_order_line(self):
        with pytest.raises(ValueError):
            SupplierOrder([], 2)

    def test_not_instance_of_order_line(self):
        with pytest.raises(ValueError):
            SupplierOrder([1], 2)  # Pylance: ignore

    def test_test_delivery_day_not_int(self, order_line):
        with pytest.raises(ValueError):
            SupplierOrder([order_line], 1.5)  # Pylance: ignore

    def test_test_delivery_day_ls_zero(self, order_line):
        with pytest.raises(ValueError):
            SupplierOrder([order_line], -2)

    def test_total_cost(self, product, product2):
        line1 = SupplierOrderLine(product, 2)
        line2 = SupplierOrderLine(product2, 3)
        supplier_order = SupplierOrder([line1, line2], 2)
        total = supplier_order.total_cost()
        expected = line1.line_cost() + line2.line_cost()
        assert total == pytest.approx(expected)

    def test_deliver_adds_stock_and_changes_status(self, product):
        warehouse = Warehouse(capacity=100)
        shop = Shop(warehouse=warehouse, budget=1000)

        line = SupplierOrderLine(product, 5)
        supplier_order = SupplierOrder([line], delivery_day=2)

        assert warehouse.get_quantity(product) == 0
        assert supplier_order.status == SupplierOrderStatus.ORDERED

        supplier_order.deliver(shop)

        assert warehouse.get_quantity(product) == 5
        assert supplier_order.status == SupplierOrderStatus.DELIVERED

    def test_deliver_cannot_be_called_twice(self, product):
        warehouse = Warehouse(capacity=100)
        shop = Shop(warehouse=warehouse, budget=1000)

        line = SupplierOrderLine(product, 5)
        supplier_order = SupplierOrder([line], delivery_day=2)

        supplier_order.deliver(shop)

        with pytest.raises(ValueError):
            supplier_order.deliver(shop)
