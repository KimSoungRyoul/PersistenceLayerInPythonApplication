from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models


from datetime import date, datetime
from typing import Any

from django.db import connections


if TYPE_CHECKING:
    from orders.models import DailyOrderReport


class OrderManager(models.Manager):
    ...


class OrderRawManger(models.Manager):
    def filter(self, blabla) -> list[Order]:
        """
            복잡한 쿼리로 데이터 조회
        :return:
        """
        return self.raw(sql="""SELECT * FROM "ORDER" WHERE id <1 """, params=[])

    def get_daily_report(self, day: date) -> DailyOrderReport:
        from orders.models import DailyOrderReport

        day_start, day_end = (
            datetime.combine(day, datetime.min.time()),
            datetime.combine(day, datetime.max.time()),
        )

        connection = connections[self.db]
        with connection.cursor() as cursor:
            cursor.execute(
                sql="""
                SELECT 
                 total_price as daily_order_cnt, 
                 total_price as hours_chicken_cnt, 
                 total_price as hours_order_cnt_with_coupon
                FROM "order" 
                WHERE created_at BETWEEN %s AND %s
            """,
                params=[day_start, day_end],
            )
            row: tuple[str, Any] = cursor.fetchone()

        return DailyOrderReport(*row)


class Order(models.Model):
    class Status(models.TextChoices):
        WAITING = "waiting", "주문 수락 대기중"
        ACCEPTED = "accepted", "주문 접수 완료"
        REJECTED = "rejected", "주문 거절"
        DELIVERY_COMPLETE = "delivery complete", "배달 완료"

    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        help_text="주문 상태값",
        default=Status.WAITING,
    )
    total_price = models.IntegerField(default=0)
    store = models.ForeignKey(to="stores.Store", on_delete=models.CASCADE)
    product_set = models.ManyToManyField(
        to="products.Product", through="OrderedProduct"
    )

    address = models.CharField(max_length=256, help_text="주문 배송지")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()
    raw_objects = OrderRawManger()

    class Meta:
        db_table = "order"
