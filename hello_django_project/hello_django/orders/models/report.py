from __future__ import annotations

from datetime import date, datetime
from typing import Any

from django.db import connections, models


class OrderReport(models.Model):
    """
        월별 통계 결과 조회용 Model ( PO(Product Owner)들이나 Manager(관리자)들이 자주본다. )
    """

    daily_order_cnt = models.IntegerField()
    weekly_order_cnt = models.IntegerField()
    monthly_order_cnt = models.IntegerField()

    class Meta:
        managed = False


class DailyOrderReportManager(models.Manager):
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


class DailyOrderReport(models.Model):
    """
        통계 결과 조회용 Model (매일보는건 개발자들이 자주 본다. )
    """

    hours_order_cnt = models.IntegerField()
    hours_chicken_cnt = models.IntegerField()
    hours_order_cnt_with_coupon = models.IntegerField()

    class Meta:
        managed = False

    def __str__(self):
        return f"DailyOrderReport \n * hours_order_cnt:{self.hours_order_cnt},\n * hours_chicken_cnt:{self.hours_chicken_cnt},\n * hours_order_cnt_with_coupon:{self.hours_order_cnt_with_coupon}\n"
