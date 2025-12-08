from src.shop_ops.product import Product
import pytest


@pytest.fixture
def product() -> Product:
    product = Product(
                      name="Mleko",
                      purchase_price=10,
                      sell_price=15,
                      space=0.1)
    return product


class TestProduct:

    def test_product_initialization(self, product):
        assert product.name == 'Mleko'
        assert product.purchase_price == 10
        assert product.sell_price == 15
        assert product.space == 0.1

    def test_product_margin(self, product):
        assert product.margin() == 5.0

    def test_product_margin_percentage(self, product):
        assert product.margin_percentage() == 0.5

    def test_sell_value_for_quantity(self, product):
        quantity = 5
        assert product.sell_value_for(quantity) == 75.0

    def test_purchase_cost_for_quantity(self, product):
        quantity = 10
        assert product.purchase_cost_for(quantity) == 100.0

    def test_products_with_same_id_are_equal(self):
        p1 = Product("Mleko", 10, 15, 0.1)
        p1.id = 1

        p2 = Product("Inna nazwa", 99, 999, 9.9)
        p2.id = 1

        assert p1 == p2

    def test_products_with_different_id_are_not_equal(self):
        p1 = Product("Mleko", 10, 15, 0.1)
        p1.id = 1

        p2 = Product("Chleb", 12, 15, 0.3)
        p2.id = 2

        assert p1 != p2

    def test_product_not_equal_to_non_product(self):
        p = Product("Mleko", 10, 15, 0.1)
        p.id = 1

        assert p != "Mleko"

    def test_equal_products_have_same_hash(self):
        p1 = Product("Mleko", 10, 15, 0.1)
        p1.id = 1

        p2 = Product("Inna nazwa", 99, 999, 9.9)
        p2.id = 1

        assert hash(p1) == hash(p2)
