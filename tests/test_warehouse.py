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
def warehouse() -> Warehouse:
    return Warehouse(capacity=100.0)


class TestWarehouse:
    def test_empty_warehouse_returns_zero_quantity(self, product, warehouse):
        assert warehouse.get_quantity(product) == 0

    def test_add_first_product(self, product, warehouse):
        warehouse.add_stock(product, 5)
        assert warehouse.get_quantity(product) == 5

    def test_add_stock_to_existing_product(self, product, warehouse):
        warehouse.add_stock(product, 5)
        warehouse.add_stock(product, 3)

        assert warehouse.get_quantity(product) == 8

    def test_negative_quantity_check(self, product, warehouse):
        with pytest.raises(ValueError):
            warehouse.add_stock(product, -999)

    def test_remove_stock_from_existignproduct(self, product, warehouse):
        warehouse.add_stock(product, 5)
        assert warehouse.get_quantity(product) == 5
        warehouse.remove_stock(product, 3)
        assert warehouse.get_quantity(product) == 2

    def test_remove_negative_quantity_check(self, product, warehouse):
        with pytest.raises(ValueError):
            warehouse.remove_stock(product, -999)
        with pytest.raises(ValueError):
            warehouse.remove_stock(product, 0)

    def test_remove_stock_to_zero(self, product, warehouse):
        warehouse.add_stock(product, 3)
        warehouse.remove_stock(product, 3)
        assert warehouse.get_quantity(product) == 0

    def test_remove_more_than_available_raises_error(self, product, warehouse):
        warehouse.add_stock(product, 3)

        with pytest.raises(ValueError):
            warehouse.remove_stock(product, 5)

    def test_remove_from_warehouse_without_product_raises_error(self,
                                                                product,
                                                                warehouse):

        with pytest.raises(ValueError):
            warehouse.remove_stock(product, 1)

    def test_get_used_space(self, product, warehouse):
        warehouse.add_stock(product, 10)
        assert warehouse.get_used_space() == pytest.approx(1.0)

    def test_get_available_space(self, product, warehouse):
        warehouse.add_stock(product, 10)
        assert warehouse.get_available_space() == pytest.approx(99.0)
