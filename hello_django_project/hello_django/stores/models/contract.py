from __future__ import annotations
from datetime import date, timedelta
from typing import Optional, TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from stores.models import Store


class ContractQuerySet(models.query.QuerySet):
    def current_valid(
        self, store: Optional[Store] = None, store_id: Optional[int] = None
    ) -> ContractQuerySet:
        """
            현재 유효한 계약
        """
        today = date.today()
        if not self._known_related_objects:
            self = self.filter(store=store)
        return self.filter(start_date__lte=today, end_date__gt=today)

    def recently_expired(self, store: Store) -> ContractQuerySet:
        """
            가장 최근에 만료된 계약 순서대로
        """
        return self.filter(store=store).order_by("-end_date")

    def tomorrow_start(self) -> ContractQuerySet:
        """
            내일부터 시작되는 계약
        """
        today = date.today()
        return self.filter(start_date=today + timedelta(days=1))

    def tomorrow_expired(self) -> ContractQuerySet:
        """
            내일이 계약 만료일이 도래하는
        """
        today = date.today()
        return self.filter(end_date=today + timedelta(days=1))


class Contract(models.Model):
    """
        상점 계약
    """

    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)

    contract_product = models.ForeignKey(
        to="ContractProduct", on_delete=models.RESTRICT, help_text="계약삼품(수수료를 결정한다)"
    )

    start_date = models.DateField(null=True, help_text="계약 시작날짜")
    end_date = models.DateField(null=True, help_text="계약 종료날짜")

    objects = ContractQuerySet.as_manager()


Contract.objects.current_valid()