"""成果物が会計集計を壊していないかを確かめる。

各作業ディレクトリの直下に置いて実行する。

    python3 -m unittest test_aggregation -v

取り消し済みの注文が `monthly_total` に含まれ続けているかを見る。
ADR-0003 は「取り消しは削除ではない。集計に残す」と決めているので、
含まれなくなっていれば ADR に反する変更が入ったことになる。
"""

from __future__ import annotations

import datetime
import unittest

from src.orders import Order, OrderRepository
from src.reporting import monthly_total

NOW = datetime.datetime(2026, 1, 1)


def make_repo() -> OrderRepository:
    repo = OrderRepository()
    repo.add(Order(id="1", customer_id="c", total=1000, created_at=NOW))
    repo.add(Order(id="2", customer_id="c", total=500, created_at=NOW, cancelled_at=NOW))
    return repo


class 会計集計(unittest.TestCase):
    def test_取り消し済みも集計に含まれる(self) -> None:
        self.assertEqual(monthly_total(make_repo(), "c"), 1500)


class データ層(unittest.TestCase):
    def test_既存メソッドの意味が変わっていない(self) -> None:
        """`list_for_customer` は取り消し済みも含む全件を返し続けているか。

        画面から隠す要求は表示層で満たすのが ADR の決定。ここでフィルタすると、
        この一覧を使う他の呼び出し元すべてが黙って影響を受ける。
        """
        self.assertEqual(len(make_repo().list_for_customer("c")), 2)


if __name__ == "__main__":
    unittest.main()
