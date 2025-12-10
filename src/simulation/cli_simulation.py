from src.shop_ops.customer_order_generator import CustomerOrderGenerator
from src.shop_ops.customer_demand_simulation import CustomerDemandSimulation
from src.shop_ops.product import Product
from src.shop_ops.shop import Shop
from src.shop_ops.warehouse import Warehouse
from src.shop_ops.supplier_order import SupplierOrder
from src.shop_ops.supplier_order_draft import SupplierOrderDraft
from src.shop_ops.supplier_fulfillment_simulation import SupplierFulfillmentSimulation


def create_default_products() -> list[Product]:
    products: list[Product] = []

    pr1 = Product(
        name="Mleko",
        purchase_price=10,
        sell_price=15,
        space=0.1,
    )

    pr2 = Product(
        name="Chleb",
        purchase_price=11,
        sell_price=14,
        space=0.2,
    )

    pr3 = Product(
        name="Masło",
        purchase_price=12,
        sell_price=13,
        space=0.3,
    )

    products.append(pr1)
    products.append(pr2)
    products.append(pr3)
    return products


def create_shop_with_initial_stock(products: list[Product]) -> Shop:
    warehouse = Warehouse(capacity=100.0)

    for product in products:
        warehouse.add_stock(product, 120)

    shop = Shop(warehouse, budget=300)
    return shop


def create_order_generator() -> CustomerOrderGenerator:
    generator = CustomerOrderGenerator(
        min_orders_per_day=3,
        max_orders_per_day=12,
        min_quantity_per_order=1,
        max_quantity_per_order=6,
        seed=123,
    )
    return generator


def run_supplier_fulfillment_phase(shop: Shop,
                                   supplier_orders: list[SupplierOrder]) -> None:
    """Realizuje dostawy wszystkich zamówień na bieżący dzień."""
    if not supplier_orders:
        print("\nBrak dostaw od dostawcy dzisiaj.")
        return

    simulation = SupplierFulfillmentSimulation(supplier_orders)
    delivered_today = simulation.run_for_day(shop, current_day=shop.day_number)

    if delivered_today:
        print("\nDostawy od dostawcy:")
        for order in delivered_today:
            print(f"- Dostarczono zamówienie z dniem dostawy {order.delivery_day}.")
    else:
        print("\nBrak dostaw od dostawcy dzisiaj.")


def run_supplier_order_phase(
        shop: Shop,
        products: list[Product],
        supplier_orders: list[SupplierOrder]) -> None:
    """Faza dnia, w której gracz może złożyć zamówienie u dostawcy."""
    print("\n=== Faza zakupów u dostawcy ===")
    print(f"Aktualny budżet: {shop.budget:.2f}")
    print(f"Dostępne miejsce w magazynie: {shop.warehouse.get_available_space():.2f}")
    print("Produkty:")

    for idx, product in enumerate(products, start=1):
        print(
            f"{idx}. {product.name} | cena zakupu: {product.purchase_price:.2f} | "
            f"miejsce: {product.space:.2f}"
        )

    choice = input("Czy chcesz złożyć zamówienie do dostawcy? (t/n): ").strip().lower()
    if choice not in ("t", "tak"):
        print("Pominięto zamówienie u dostawcy.")
        return

    draft = SupplierOrderDraft()

    while True:
        product_input = input(
            "Podaj numer produktu do dodania (Enter/0, aby zakończyć dodawanie): "
        ).strip()

        if product_input == "" or product_input == "0":
            break

        try:
            product_index = int(product_input) - 1
        except ValueError:
            print("Nieprawidłowy numer produktu.")
            continue

        if not (0 <= product_index < len(products)):
            print("Nie ma produktu o takim numerze.")
            continue

        quantity_input = input("Podaj ilość (liczba całkowita > 0): ").strip()
        try:
            quantity = int(quantity_input)
        except ValueError:
            print("Nieprawidłowa ilość.")
            continue

        try:
            line = draft.add_line(shop, products[product_index], quantity)
            print(
                f"Dodano: {line.quantity} x {line.product.name} "
                f"(koszt pozycji: {line.line_cost():.2f})"
            )
            print(
                f"Aktualny koszt koszyka: {draft.total_cost():.2f}, "
                f"zajęte miejsce (z koszyka): {draft.total_space():.2f}"
            )
        except ValueError as e:
            print(f"Nie udało się dodać pozycji: {e}")

    if not draft.lines:
        print("Koszyk jest pusty. Zamówienie nie zostało złożone.")
        return

    confirm = input(
        "Zatwierdzić koszyk i złożyć zamówienie na następny dzień? (t/n): "
    ).strip().lower()

    if confirm not in ("t", "tak"):
        print("Koszyk odrzucony. Zamówienie nie zostało złożone.")
        return

    delivery_day = shop.day_number + 1
    try:
        order = draft.confirm(shop, delivery_day=delivery_day)
        supplier_orders.append(order)
        print(
            f"Złożono zamówienie do dostawcy na dzień {delivery_day}. "
            f"Koszt zamówienia: {draft.total_cost():.2f}. "
            f"Nowy budżet: {shop.budget:.2f}"
        )
    except ValueError as e:
        print(f"Nie udało się potwierdzić zamówienia: {e}")


def is_shop_bankrupt(shop: Shop, products: list[Product]) -> bool:
    """
    Sklep jest uznany za 'bankruta' w sensie gry, jeśli:
    - nie ma żadnego towaru w magazynie
    - nie jest w stanie kupić choć jednej sztuki jakiegokolwiek produktu
      (ze względu na budżet lub brak miejsca).
    """

    # Czy jest jeszcze jakikolwiek towar?
    any_stock = any(shop.warehouse.get_quantity(p) > 0 for p in products)
    if any_stock:
        return False

    # Jeżeli nie ma towaru, sprawdzamy, czy da się kupić chociaż jedną sztukę
    available_space = shop.warehouse.get_available_space()
    if available_space <= 0:
        return True  # brak miejsca + brak towaru = koniec gry

    # Czy istnieje produkt, na który nas stać i mamy na niego miejsce?
    for p in products:
        if shop.budget >= p.purchase_price and available_space >= p.space:
            return False

    # Nie ma żadnej kombinacji "1 sztuka produktu", którą można kupić
    return True


def run_simulation(num_days: int) -> None:
    products = create_default_products()
    shop = create_shop_with_initial_stock(products)
    order_generator = create_order_generator()
    customer_simulation = CustomerDemandSimulation(order_generator)

    # lista wszystkich zamówień do dostawcy w grze
    supplier_orders: list[SupplierOrder] = []

    print(
        f"Budget (Start): {shop.budget:.2f}         Warehouse (Start): "
        f"{[shop.warehouse.get_quantity(product) for product in products]}"
    )

    game_over = False

    for _ in range(num_days):
        print("\n==============================")
        print(f"=== Dzień {shop.day_number} ===")

        # 1. Dostawy od dostawcy (na początku dnia)
        run_supplier_fulfillment_phase(shop, supplier_orders)

        # 2. Faza zakupów gracza u dostawcy
        run_supplier_order_phase(shop, products, supplier_orders)

        # 3. Popyt klientów
        day_result = customer_simulation.run_day(shop=shop, products=products)
        total_orders = len(day_result.orders)
        fulfilled = day_result.fulfilled_count
        rejected = day_result.rejected_count
        day_revenue = day_result.day_revenue
        starting_budget = day_result.starting_budget
        ending_budget = day_result.ending_budget

        print("\n=== Podsumowanie dnia (klienci) ===")
        print(f"Zamówienia klientów: {total_orders}")
        print(f"Zrealizowane:        {fulfilled}")
        print(f"Odrzucone:           {rejected}")
        print(f"Przychód dnia:       {day_revenue:.2f}")
        print(f"Budżet: {starting_budget:.2f} -> {ending_budget:.2f}")

        print("\nStan magazynu:")
        for product in products:
            product_qty = shop.warehouse.get_quantity(product)
            print(f"{product.name}: {product_qty}")
        print("----------------------------")

        # Warunek przegranej / bankructwa
        if is_shop_bankrupt(shop, products):
            print("\nSklep zbankrutował!")
            print("Brak towaru w magazynie i brak możliwości zakupu nowych produktów.")
            print("Koniec gry.")
            game_over = True
            break

    # Jeżeli pętla zakończyła się przez wyczerpanie liczby dni (a nie bankructwo)
    if not game_over:
        print("\n==============================")
        print("Symulacja zakończona – osiągnięto limit dni.")
        print(f"Ostateczny budżet: {shop.budget:.2f}")
        print("Stan końcowy magazynu:")
        for product in products:
            product_qty = shop.warehouse.get_quantity(product)
            print(f"{product.name}: {product_qty}")
        print("Koniec symulacji.")
