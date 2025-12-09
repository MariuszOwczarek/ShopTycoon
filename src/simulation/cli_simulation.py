from src.shop_ops.customer_order_generator import CustomerOrderGenerator
from src.shop_ops.day_simulation import DaySimulation
from src.shop_ops.product import Product
from src.shop_ops.shop import Shop
from src.shop_ops.warehouse import Warehouse


def create_default_products() -> list[Product]:
    products: list[Product] = []
    pr1 = Product(name="Mleko",
                  purchase_price=10,
                  sell_price=15,
                  space=0.1)

    pr2 = Product(name="Chleb",
                  purchase_price=11,
                  sell_price=14,
                  space=0.2)

    pr3 = Product(name="Masło",
                  purchase_price=12,
                  sell_price=13,
                  space=0.3)

    products.append(pr1)
    products.append(pr2)
    products.append(pr3)
    return products


def create_shop_with_initial_stock(products: list[Product]) -> Shop:
    warehouse = Warehouse(capacity=500.0)

    for product in products:
        warehouse.add_stock(product, 30)

    shop = Shop(warehouse, budget=1000)
    return shop


def create_order_generator() -> CustomerOrderGenerator:
    generator = CustomerOrderGenerator(3, 15, 1, 8, seed=123)
    return generator


def run_simulation(num_days: int):
    products = create_default_products()
    shop = create_shop_with_initial_stock(products)
    order_generator = create_order_generator()
    simulation = DaySimulation(order_generator)

    print(f"Budget (Start): {shop.budget}         Warehouse (Start):"
          f"{[shop.warehouse.get_quantity(product) for product in products]}")

    for _ in range(num_days):
        day_result = simulation.run_day(shop=shop, products=products)
        total_orders = len(day_result.orders)
        fulfilled = day_result.fulfilled_count
        rejected = day_result.rejected_count
        day_revenue = day_result.day_revenue
        starting_budget = day_result.starting_budget
        ending_budget = day_result.ending_budget

        print(f'=== Dzień {day_result.day_number} ===')
        print(f'Zamówienia: {total_orders}')
        print(f'Zrealizowane: {fulfilled}')
        print(f'Odrzucone:    {rejected}')
        print(f'Przychód dnia:  {day_revenue:.2f}')
        print(f'Budżet: {starting_budget:.2f} -> {ending_budget:.2f}')

        print('Stan magazynu:')
        for product in products:
            product_qty = shop.warehouse.get_quantity(product)
            print(f'{product.name}: {product_qty}')
        print('----------------------------')
