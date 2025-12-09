
from dataclasses import dataclass
from src.shop_ops.customer_order import CustomerOrder


@dataclass
class DayResult:
    day_number: int
    orders: list[CustomerOrder]
    fulfilled_count: int
    rejected_count: int
    day_revenue: float
    starting_budget: float
    ending_budget: float
