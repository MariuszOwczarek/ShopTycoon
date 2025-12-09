from src.shop_ops.warehouse import Warehouse


class Shop:
    def __init__(self, warehouse: Warehouse, budget: float = 10000) -> None:
        self.warehouse: Warehouse = warehouse
        self.budget: float = budget
        self.day_number: int = 1
        self.today_revenue: float = 0
        self.revenue_history: list[float] = []

    def register_sale(self, amount: float) -> None:
        self.today_revenue += amount
        self.budget += amount

    def get_today_revenue(self) -> float:
        return self.today_revenue

    def get_total_revenue(self) -> float:
        total_revenue = 0
        for revenue in self.revenue_history:
            total_revenue += revenue
        return total_revenue
        # [total_revenue += revenue for revenue in self.revenue_history]

    def is_bankrupt(self) -> bool:
        if self.budget < 0:
            return True
        return False

    def start_new_day(self) -> None:
        self.revenue_history.append(self.today_revenue)
        self.day_number += 1
        self.today_revenue = 0
