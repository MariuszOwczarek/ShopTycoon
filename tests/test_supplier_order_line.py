import pytest
from src.shop_ops.product import Product
from src.shop_ops.supplier_order_line import SupplierOrderLine


@pytest.fixture
def product() -> Product:
    return Product(
        name="Mleko",
        purchase_price=10,
        sell_price=15,
        space=0.1,
    )


class TestSupplierOrderLine:
    def test_supplier_order_line_initialization(self, product):
        quantity = 10
        supplier_order_line = SupplierOrderLine(product, quantity)

        assert supplier_order_line.product is product
        assert supplier_order_line.quantity == 10
        assert supplier_order_line.unit_price == product.purchase_price

    def test_supplier_order_line_cost(self, product):
        supplier_order_line = SupplierOrderLine(product, 10)
        assert supplier_order_line.line_cost() == pytest.approx(100.0)

    def test_supplier_order_line_invalid_quantity_zero(self, product):
        with pytest.raises(ValueError):
            SupplierOrderLine(product, 0)

    def test_supplier_order_line_invalid_quantity_negative(self, product):
        with pytest.raises(ValueError):
            SupplierOrderLine(product, -5)

    def test_supplier_order_line_invalid_quantity_float(self, product):
        with pytest.raises(ValueError):
            SupplierOrderLine(product, 1.5)
