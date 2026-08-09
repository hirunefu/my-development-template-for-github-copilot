"""集計。会計側がこの結果を使う。"""
from __future__ import annotations
from .orders import OrderRepository


def monthly_total(repo: OrderRepository, customer_id: str) -> int:
    return sum(o.total for o in repo.list_for_customer(customer_id))
