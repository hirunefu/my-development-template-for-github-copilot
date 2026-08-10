"""請求の管理。注文とは独立して状態を持つ。"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Invoice:
    id: str
    order_id: str
    amount: int
    issued_at: datetime
    voided_at: datetime | None = None


class InvoiceRepository:
    def __init__(self) -> None:
        self._invoices: dict[str, Invoice] = {}

    def add(self, invoice: Invoice) -> None:
        self._invoices[invoice.id] = invoice

    def for_order(self, order_id: str) -> list[Invoice]:
        return [i for i in self._invoices.values() if i.order_id == order_id]
