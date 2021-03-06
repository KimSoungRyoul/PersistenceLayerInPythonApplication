from __future__ import annotations

from datetime import time

from django.db import models


class Store(models.Model):
    class StoreType(models.TextChoices):
        FOOD = "food", "배달음식"
        GROCERY = "grocery", "식료품/가공식품"
        PET_FOOD = "pet_food", "반려동물음식"

    name = models.CharField(max_length=128, help_text="음식점 가게명")
    owner = models.ForeignKey(to="users.User", on_delete=models.CASCADE, null=True)
    tel_num = models.CharField(max_length=16, help_text="음식점 연락처")
    created_at = models.DateTimeField(auto_now_add=True)
    store_type = models.CharField(
        choices=StoreType.choices, help_text="상점 유형", max_length=32
    )

    class Meta:
        db_table = "store"

    def is_open(self) -> bool:
        return self.businesshour_set.exists()


class BusinessHour(models.Model):
    """
        영업시간
    """

    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)

    begin_time = models.TimeField(default=time(0, 0), help_text="영업 시작 시간")
    end_time = models.TimeField(default=time(0, 0), help_text="영업 종료 시간")
