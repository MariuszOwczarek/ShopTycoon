from src.shop_ops.customer_order import CustomerOrder, CustomerOrderStatus
from src.shop_ops.product import Product
from src.shop_ops.warehouse import Warehouse
import pytest


@pytest.fixture
def product() -> Product:
    product = Product(name="Mleko",
                      purchase_price=10,
                      sell_price=15,
                      space=0.1)
    return product


@pytest.fixture
def customer_order(product) -> CustomerOrder:
    order = CustomerOrder(product, 5)
    return order


@pytest.fixture
def warehouse() -> Warehouse:
    return Warehouse(capacity=100.0)


class TestCustomerOrder:
    def test_total_order_value(self, customer_order):
        assert customer_order.total_order_value() == pytest.approx(75.0)

    def test_can_be_fulfilled(self, product, warehouse, customer_order):
        warehouse.add_stock(product, 5)
        assert customer_order.can_be_fulfilled(warehouse) is True

    def test_fulfill_status_change(self, product, warehouse, customer_order):
        warehouse.add_stock(product, 5)
        customer_order.fulfill_order(warehouse)
        assert warehouse.get_quantity(product) == 0
        assert customer_order.status == CustomerOrderStatus.FULFILLED
        assert customer_order.total_order_value() == pytest.approx(75.0)

    def test_reject_status_change(self, customer_order):
        customer_order.reject_order()
        assert customer_order.status == CustomerOrderStatus.REJECTED

    def test_customer_order_lte_zero(self,
                                     product):

        with pytest.raises(ValueError):
            CustomerOrder(product, 0)
            CustomerOrder(product, -10)

    def test_cannot_be_fulfilled_insufficient_stock(self, product, warehouse):
        order = CustomerOrder(product, 5)
        warehouse.add_stock(product, 3)
        assert order.can_be_fulfilled(warehouse) is False

    def test_fraises_error_when_insufficient_stock(self, product, warehouse):
        order = CustomerOrder(product, 5)
        with pytest.raises(ValueError):
            order.fulfill_order(warehouse)

    def test_new_order_has_pending_status(self, product):
        order = CustomerOrder(product, 5)
        assert order.status == CustomerOrderStatus.PENDING
