from src.shop_ops.product import Product


class SupplierOrderLine:
    def __init__(self, product: Product, quantity: int) -> None:

        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        self.product: Product = product
        self.quantity: int = quantity
        self.unit_price: float = product.purchase_price

    def line_cost(self) -> float:
        return self.unit_price * self.quantity
