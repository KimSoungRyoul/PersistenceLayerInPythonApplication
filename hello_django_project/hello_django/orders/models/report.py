from __future__ import annotations

from django.db import models


class OrderReport(models.Model):
    """
        월별 통계 결과 조회용 Model ( PO(Product Owner)들이나 Manager(관리자)들이 자주본다. )
    """
    daily_order_cnt = models.IntegerField()
    weekly_order_cnt = models.IntegerField()
    monthly_order_cnt = models.IntegerField()

    class Meta:
        managed = False


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
