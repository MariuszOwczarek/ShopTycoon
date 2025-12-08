from src.shop_ops.product import Product
from src.shop_ops.stock_item import StockItem
import pytest


@pytest.fixture
def product() -> Product:
    product = Product(name="Mleko",
                      purchase_price=10,
                      sell_price=15,
                      space=0.1)
    return product


@pytest.fixture
def stock_item(product) -> StockItem:
    return StockItem(product=product,
                     quantity=5)


class TestInventoryItem:

    def test_inventory_item_initialization(self,
                                           stock_item,
                                           product):

        item = stock_item
        product = product

        assert item.product is product
        assert item.quantity == 5

    def test_inventory_item_increase_quantity(self,
                                              stock_item):

        item = stock_item
        item.increase(2)

        assert item.quantity == 7

    def test_inventory_item_decrease_quantity(self,
                                              stock_item):

        item = stock_item
        item.decrease(4)

        assert item.quantity == 1

    def test_inventory_item_incr_decr_qty(self, stock_item):

        item = stock_item
        assert item.quantity == 5
        item.increase(4)
        assert item.quantity == 9
        item.decrease(3)
        assert item.quantity == 6

    def test_inventory_item_total_sell_value(self, stock_item):
        item = stock_item
        assert item.total_sell_value() == 75.0

    def test_inventory_item_total_purchase_cost(self, stock_item):
        item = stock_item
        assert item.total_purchase_cost() == 50.0
