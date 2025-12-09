import pytest
from src.shop_ops.product import Product
from src.shop_ops.customer_order_generator import CustomerOrderGenerator
from src.shop_ops.customer_order import CustomerOrderStatus


def create_products() -> list[Product]:
    products: list[Product] = []
    pr1 = Product(name="Produkt_1",
                  purchase_price=10,
                  sell_price=15,
                  space=0.1)

    pr2 = Product(name="Produkt_2",
                  purchase_price=11,
                  sell_price=14,
                  space=0.2)

    pr3 = Product(name="Produkt_3",
                  purchase_price=12,
                  sell_price=13,
                  space=0.3)

    products.append(pr1)
    products.append(pr2)
    products.append(pr3)
    return products


class TestCustomerOrderGenerator:
    def test_number_of_daily_orders_beween_min_and_max(self):
        products = create_products()
        generator = CustomerOrderGenerator(min_orders_per_day=1,
                                           max_orders_per_day=5,
                                           min_quantity_per_order=1,
                                           max_quantity_per_order=5,
                                           seed=123)

        orders = generator.generate_orders(products)
        assert 1 <= len(orders) <= 5
        assert (generator.min_orders_per_day <=
                len(orders) <=
                generator.max_orders_per_day)

    def test_min_orders_per_day_cannot_be_negative(self):
        with pytest.raises(ValueError):
            CustomerOrderGenerator(
                min_orders_per_day=-1,
                max_orders_per_day=5,
                min_quantity_per_order=1,
                max_quantity_per_order=5,
                seed=123)

    def test_max_orders_per_day_must_be_greater_than_min(self):
        with pytest.raises(ValueError):
            CustomerOrderGenerator(
                min_orders_per_day=3,
                max_orders_per_day=3,
                min_quantity_per_order=1,
                max_quantity_per_order=5,
                seed=123)

    def test_min_quantity_per_order_must_be_greater_than_zero(self):
        with pytest.raises(ValueError):
            CustomerOrderGenerator(
                min_orders_per_day=1,
                max_orders_per_day=5,
                min_quantity_per_order=0,
                max_quantity_per_order=5,
                seed=123)

    def test_max_quantity_per_order_must_be_greater_or_equal_min(self):
        with pytest.raises(ValueError):
            CustomerOrderGenerator(
                min_orders_per_day=1,
                max_orders_per_day=5,
                min_quantity_per_order=5,
                max_quantity_per_order=4,
                seed=123)

    def test_empty_product_list(self):
        generator = CustomerOrderGenerator(min_orders_per_day=1,
                                           max_orders_per_day=5,
                                           min_quantity_per_order=1,
                                           max_quantity_per_order=5,
                                           seed=123)

        with pytest.raises(ValueError):
            generator.generate_orders([])

    def test_generated_quantities_are_within_range(self):
        products = create_products()

        generator = CustomerOrderGenerator(
            min_orders_per_day=5,
            max_orders_per_day=6,
            min_quantity_per_order=2,
            max_quantity_per_order=4,
            seed=123
        )

        orders = generator.generate_orders(products)

        assert len(orders) == 5

        for order in orders:
            assert 2 <= order.quantity <= 4

    def test_all_orders_use_products_from_input_list(self):
        products = create_products()

        generator = CustomerOrderGenerator(
            min_orders_per_day=3,
            max_orders_per_day=5,
            min_quantity_per_order=1,
            max_quantity_per_order=10,
            seed=123
        )

        orders = generator.generate_orders(products)

        for order in orders:
            assert order.product in products

    def test_all_generated_orders_have_pending_status(self):
        products = create_products()

        generator = CustomerOrderGenerator(
            min_orders_per_day=3,
            max_orders_per_day=5,
            min_quantity_per_order=1,
            max_quantity_per_order=10,
            seed=123
        )

        orders = generator.generate_orders(products)

        for order in orders:
            assert order.status == CustomerOrderStatus.PENDING

    def test_generator_is_deterministic_for_same_seed(self):
        products = create_products()

        generator1 = CustomerOrderGenerator(
            min_orders_per_day=3,
            max_orders_per_day=5,
            min_quantity_per_order=1,
            max_quantity_per_order=10,
            seed=123
        )

        generator2 = CustomerOrderGenerator(
            min_orders_per_day=3,
            max_orders_per_day=5,
            min_quantity_per_order=1,
            max_quantity_per_order=10,
            seed=123
        )

        orders1 = generator1.generate_orders(products)
        orders2 = generator2.generate_orders(products)

        assert len(orders1) == len(orders2)

        for o1, o2 in zip(orders1, orders2):
            assert o1.product == o2.product
            assert o1.quantity == o2.quantity
            assert o1.status == o2.status
