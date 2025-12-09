import pytest
from src.shop_ops.day_simulation import DaySimulation
from src.shop_ops.customer_order import CustomerOrder, CustomerOrderStatus
from src.shop_ops.warehouse import Warehouse
from src.shop_ops.product import Product
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
def warehouse() -> Warehouse:
    return Warehouse(capacity=100.0)


@pytest.fixture
def shop(warehouse) -> Shop:
    return Shop(warehouse=warehouse)


class FakeOrderGenerator:
    def __init__(self, orders_to_return):
        self._orders = orders_to_return

    def generate_orders(self, products):
        return list(self._orders)


class TestDaySimulation:
    def test_all_orders_may_be_delivered(self, product, warehouse, shop):
        # Arrange
        shop.day_number = 3
        warehouse.add_stock(product=product, quantity=100)

        orders = [
            CustomerOrder(product, 5),
            CustomerOrder(product, 5),
            CustomerOrder(product, 5),
        ]

        order_generator = FakeOrderGenerator(orders)
        simulation = DaySimulation(order_generator)

        starting_budget = shop.budget
        total_quantity = sum(order.quantity for order in orders)
        expected_remaining_stock = (warehouse.get_quantity(product)
                                    - total_quantity)

        # Act
        result = simulation.run_day(shop=shop, products=[product])

        # Assert – wszystkie zamówienia zrealizowane
        for order in orders:
            assert order.status == CustomerOrderStatus.FULFILLED

        expected_revenue = sum(order.total_order_value() for order in orders)
        expected_ending_budget = starting_budget + expected_revenue

        # Magazyn
        assert warehouse.get_quantity(product) == expected_remaining_stock

        # Budżet sklepu
        assert shop.budget == expected_ending_budget

        # DayResult – liczby zamówień i przychód
        assert result.fulfilled_count == len(orders)
        assert result.rejected_count == 0
        assert result.day_revenue == expected_revenue

        # DayResult – numer dnia
        assert result.day_number == 3

        # Shop – nowy dzień
        assert shop.day_number == 4

        # Shop – historia przychodów i today_revenue
        assert result.day_revenue in shop.revenue_history
        assert shop.revenue_history[-1] == expected_revenue
        assert shop.get_today_revenue() == 0

        # DayResult – budżety
        assert result.starting_budget == starting_budget
        assert result.ending_budget == expected_ending_budget

    def test_some_orders_are_rejected_when_stock_is_insufficient(
        self, product, warehouse, shop
    ):
        # Arrange
        shop.day_number = 1
        warehouse.add_stock(product=product, quantity=10)  # mniej niż potrzeba

        orders = [
            CustomerOrder(product, 5),
            CustomerOrder(product, 5),
            CustomerOrder(product, 5),
        ]  # razem 15, stock = 10

        order_generator = FakeOrderGenerator(orders)
        simulation = DaySimulation(order_generator)

        starting_budget = shop.budget
        starting_stock = warehouse.get_quantity(product)

        # Act
        result = simulation.run_day(shop=shop, products=[product])

        # Assert – statusy zamówień
        fulfilled_orders = [o for o in orders if
                            o.status == CustomerOrderStatus.FULFILLED]
        rejected_orders = [o for o in orders if
                           o.status == CustomerOrderStatus.REJECTED]

        # Przy obecnej implementacji – 2 fulfilled, 1 rejected
        assert len(fulfilled_orders) >= 1
        assert len(rejected_orders) >= 1
        assert len(fulfilled_orders) + len(rejected_orders) == len(orders)

        # Magazyn nie schodzi poniżej zera
        fulfilled_quantity = sum(o.quantity for o in fulfilled_orders)
        expected_remaining_stock = starting_stock - fulfilled_quantity
        assert expected_remaining_stock >= 0
        assert warehouse.get_quantity(product) == expected_remaining_stock

        # Przychód i budżet tylko z zrealizowanych zamówień
        expected_revenue = sum(o.total_order_value() for o in fulfilled_orders)
        expected_ending_budget = starting_budget + expected_revenue

        assert result.day_revenue == expected_revenue
        assert shop.budget == expected_ending_budget

        # DayResult – liczby zamówień
        assert result.fulfilled_count == len(fulfilled_orders)
        assert result.rejected_count == len(rejected_orders)

        # Shop – dzień i historia przychodów
        assert result.day_number == 1
        assert shop.day_number == 2
        assert shop.revenue_history[-1] == expected_revenue
        assert shop.get_today_revenue() == 0

        # DayResult – budżety
        assert result.starting_budget == starting_budget
        assert result.ending_budget == expected_ending_budget

    def test_no_orders_results_in_zero_revenue_and_still_stock_and_budget(
        self, product, warehouse, shop
    ):
        # Arrange
        shop.day_number = 10
        # Magazyn może mieć jakiś stan, ale nie ma zamówień
        warehouse.add_stock(product=product, quantity=50)

        orders: list[CustomerOrder] = []  # brak zamówień

        order_generator = FakeOrderGenerator(orders)
        simulation = DaySimulation(order_generator)

        starting_budget = shop.budget
        starting_stock = warehouse.get_quantity(product)

        # Act
        result = simulation.run_day(shop=shop, products=[product])

        # Assert – brak zmian w magazynie i budżecie
        assert warehouse.get_quantity(product) == starting_stock
        assert shop.budget == starting_budget

        # DayResult – brak zamówień i przychodu
        assert result.fulfilled_count == 0
        assert result.rejected_count == 0
        assert result.day_revenue == 0

        # DayResult – numer dnia
        assert result.day_number == 10

        # Shop – przesunięcie dnia
        assert shop.day_number == 11

        # Historia przychodów – wpis 0 za ten dzień
        assert shop.revenue_history[-1] == 0
        assert shop.get_today_revenue() == 0

        # DayResult – budżety
        assert result.starting_budget == starting_budget
        assert result.ending_budget == starting_budget
