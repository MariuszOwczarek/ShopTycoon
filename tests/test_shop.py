import pytest
from src.shop_ops.warehouse import Warehouse
from src.shop_ops.shop import Shop


@pytest.fixture
def warehouse() -> Warehouse:
    return Warehouse(capacity=100.0)


@pytest.fixture
def shop(warehouse) -> Shop:
    return Shop(warehouse=warehouse,
                budget=10000)


class TestShop:
    def test_shop_testing(self, shop):
        assert shop.day_number == 1
        assert shop.today_revenue == 0
        assert shop.budget == pytest.approx(10000)

    def test_register_sale(self, shop):
        shop.register_sale(10)
        assert shop.today_revenue == 10
        assert shop.budget == 10010

    def test_start_new_day(self, shop):
        shop.start_new_day()
        assert shop.day_number - len(shop.revenue_history) == 1
        assert shop.day_number == 2
        assert shop.today_revenue == 0

    def test_historical_revenue(self, shop):
        shop.register_sale(100)
        shop.start_new_day()
        assert len(shop.revenue_history) == 1
        assert shop.revenue_history[0] == 100

    def test_get_total_revenue(self, shop):
        shop.register_sale(100)
        shop.start_new_day()
        shop.register_sale(50)
        shop.start_new_day()
        assert shop.get_total_revenue() == 150

    def test_is_bankrupt(self, shop):
        shop.budget = -100
        assert shop.is_bankrupt() is True
