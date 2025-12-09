from src.shop_ops.customer_order_generator import CustomerOrderGenerator
from src.shop_ops.day_result import DayResult


class DaySimulation:
    def __init__(self, order_generator: CustomerOrderGenerator):
        self._generator = order_generator

    def run_day(self, shop, products):
        current_day = shop.day_number
        starting_budget = shop.budget
        orders = self._generator.generate_orders(products)
        fulfilled_count = 0
        rejected_count = 0
        for order in orders:
            if order.can_be_fulfilled(shop.warehouse):
                order.fulfill_order(shop.warehouse)
                shop.register_sale(order.total_order_value())
                fulfilled_count += 1
            else:
                order.reject_order()
                rejected_count += 1

        day_revenue = shop.get_today_revenue()
        shop.start_new_day()
        ending_budget = shop.budget
        day_result = DayResult(day_number=current_day,
                               orders=orders,
                               fulfilled_count=fulfilled_count,
                               rejected_count=rejected_count,
                               day_revenue=day_revenue,
                               starting_budget=starting_budget,
                               ending_budget=ending_budget)
        return day_result
