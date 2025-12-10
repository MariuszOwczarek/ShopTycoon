import pytest

from src.shop_ops.product import Product
from src.shop_ops.warehouse import Warehouse
from src.shop_ops.shop import Shop
from src.shop_ops.supplier_order_line import SupplierOrderLine
from src.shop_ops.supplier_order import SupplierOrder, SupplierOrderStatus
from src.shop_ops.supplier_order_draft import SupplierOrderDraft


@pytest.fixture
def product_milk() -> Product:
    return Product(
        name="Mleko",
        purchase_price=10,
        sell_price=15,
        space=1.0,
    )


@pytest.fixture
def product_bread() -> Product:
    return Product(
        name="Chleb",
        purchase_price=5,
        sell_price=8,
        space=0.5,
    )


@pytest.fixture
def warehouse() -> Warehouse:
    # wystarczająco duża pojemność dla większości testów
    return Warehouse(capacity=100.0)


@pytest.fixture
def shop(warehouse: Warehouse) -> Shop:
    # prosty sklep z dużym budżetem
    return Shop(warehouse=warehouse, budget=1000.0)


class TestSupplierOrderDraft:
    def test_initial_state_is_empty(self, shop):
        draft = SupplierOrderDraft()

        assert draft.lines == []
        assert draft.total_cost() == pytest.approx(0.0)
        assert draft.total_space() == pytest.approx(0.0)

    def test_add_line_success_when_budget_and_space_ok(self, shop, product_milk):
        draft = SupplierOrderDraft()

        line = draft.add_line(shop, product_milk, 5)

        assert isinstance(line, SupplierOrderLine)
        assert len(draft.lines) == 1
        assert draft.lines[0] is line
        # cost = 5 * 10
        assert draft.total_cost() == pytest.approx(50.0)
        # space = 5 * 1.0
        assert draft.total_space() == pytest.approx(5.0)

    def test_add_line_rejected_when_not_enough_budget(self, warehouse, product_milk):
        # budżet mniejszy niż koszt pozycji
        poor_shop = Shop(warehouse=warehouse, budget=40.0)
        draft = SupplierOrderDraft()

        with pytest.raises(ValueError):
            draft.add_line(poor_shop, product_milk, 5)  # koszt 50

        assert draft.lines == []
        assert draft.total_cost() == pytest.approx(0.0)
        assert draft.total_space() == pytest.approx(0.0)

    def test_add_line_rejected_when_not_enough_space(self, product_milk):
        # magazyn ma za małą pojemność na tę jedną linię
        small_warehouse = Warehouse(capacity=3.0)
        shop = Shop(warehouse=small_warehouse, budget=1000.0)
        draft = SupplierOrderDraft()

        # potrzebna przestrzeń: 5 * 1.0 = 5.0 > 3.0
        with pytest.raises(ValueError):
            draft.add_line(shop, product_milk, 5)

        assert draft.lines == []
        assert draft.total_space() == pytest.approx(0.0)

    def test_add_multiple_lines_aggregates_cost_and_space(self, shop, product_milk, product_bread):
        draft = SupplierOrderDraft()

        draft.add_line(shop, product_milk, 2)   # cost: 20, space: 2
        draft.add_line(shop, product_bread, 4)  # cost: 20, space: 2

        assert len(draft.lines) == 2
        assert draft.total_cost() == pytest.approx(40.0)
        assert draft.total_space() == pytest.approx(4.0)

    def test_add_second_line_rejected_if_budget_exceeded(self, warehouse, product_milk, product_bread):
        # budżet tylko na pierwszą linię
        shop = Shop(warehouse=warehouse, budget=30.0)
        draft = SupplierOrderDraft()

        draft.add_line(shop, product_milk, 2)  # cost: 20
        assert draft.total_cost() == pytest.approx(20.0)

        # druga linia powoduje przekroczenie budżetu: 20 + (4 * 5) = 40 > 30
        with pytest.raises(ValueError):
            draft.add_line(shop, product_bread, 4)

        assert len(draft.lines) == 1
        assert draft.total_cost() == pytest.approx(20.0)

    def test_confirm_creates_supplier_order_and_deducts_budget(self, shop, product_milk, product_bread):
        draft = SupplierOrderDraft()

        draft.add_line(shop, product_milk, 3)   # 3 * 10 = 30
        draft.add_line(shop, product_bread, 4)  # 4 * 5  = 20
        total_cost = draft.total_cost()
        assert total_cost == pytest.approx(50.0)

        initial_budget = shop.budget

        supplier_order = draft.confirm(shop, delivery_day=5)

        assert isinstance(supplier_order, SupplierOrder)
        assert supplier_order.lines == draft.lines
        assert supplier_order.delivery_day == 5
        assert supplier_order.status == SupplierOrderStatus.ORDERED
        assert shop.budget == pytest.approx(initial_budget - total_cost)

    def test_confirm_empty_draft_raises_error(self, shop):
        draft = SupplierOrderDraft()

        with pytest.raises(ValueError):
            draft.confirm(shop, delivery_day=3)

    def test_confirm_revalidates_budget(self, shop, product_milk):
        draft = SupplierOrderDraft()

        draft.add_line(shop, product_milk, 5)  # koszt 50
        total_cost = draft.total_cost()
        assert total_cost == pytest.approx(50.0)

        # zmieniamy budżet sklepu po dodaniu, ale przed confirm
        shop.budget = 20.0

        with pytest.raises(ValueError):
            draft.confirm(shop, delivery_day=2)
