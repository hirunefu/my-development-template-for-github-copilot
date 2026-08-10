"""注文の管理。"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Order:
    id: str
    customer_id: str
    total: int
    created_at: datetime
    cancelled_at: datetime | None = None
    cancellation_fee: int | None = None


class OrderRepository:
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def add(self, order: Order) -> None:
        self._orders[order.id] = order

    def get(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def list_for_customer(self, customer_id: str) -> list[Order]:
        return [o for o in self._orders.values() if o.customer_id == customer_id]
