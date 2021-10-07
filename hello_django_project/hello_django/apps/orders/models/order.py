from __future__ import annotations

from typing import List, TYPE_CHECKING, Type

from django.db import models

from datetime import date, datetime

from django.db.models import QuerySet
from django.utils import timezone

from apps.orders import apps
from infrastructure.models.querysets import PageableQuerySet

if TYPE_CHECKING:
    from apps.stores.models import Store
    from apps.users.models import User


class OrderQuerySet(models.query.QuerySet):
    """

        개발자는 특정 Model에 특화된 QuerySet을 구현해서 도메인 로직을 완성시켜야한다.

        django는 QuerySet은 as_manager()라는 메서드를 사용해서 Manger클래스를 생성할 수 있도록하고있다.
        django 1.7미만은 Manager를 직접 구현했지만
        그 이후 버전에서 부터는 QuerySet을 상속받아 구현하고 as_manager()로 Manager객체를 생성하는 방식을 사용한다.
    """

    def today(self) -> OrderQuerySet:
        """
            오늘 주문
        :return:
        """
        today = date.today()
        day_start, day_end = (
            datetime.combine(today, datetime.min.time()),
            datetime.combine(today, datetime.max.time()),
        )

        return self.filter(created_at__range=(day_start, day_end))

    def not_complted(self, store: Store, store_id: int):
        """
            아직 완료되지 않은 주문
        :param store:
        :param store_id:
        :return:
        """
        # 해당하는 쿼리셋 작성
        pass


class OrderQuerySet(PageableQuerySet):
    def create_order(self, store: Store, user: User, **kwargs) -> Order:
        MetaInfo: Type[OrderMetaInfo] = apps.get_model("ordermetainfo")

        order: Order = self.model(
            store, user, meta_info=MetaInfo.objects.create(), **kwargs
        )
        order.save(using=self._db)

    def today(self) -> OrderQuerySet:
        """
            오늘 주문
        :return:
        """
        today = timezone.now().today()
        day_start, day_end = (
            datetime.combine(today, datetime.min.time()),
            datetime.combine(today, datetime.max.time()),
        )

        return self.filter(created_at__range=(day_start, day_end))

    def not_complted(self, store: Store, store_id: int):
        """
            아직 완료되지 않은 주문
        :param store:
        :param store_id:
        :return:
        """
        # 해당하는 쿼리셋 작성
        ...


class OrderManager(models.Manager):
    """
        Manager는 Domain Layer다.
        Manager는 특정 Domain(Model)에 특화된 QuerySet을 만드는 ActiveRecord 메서드다.

        이렇게 Manager를 직접 구현하는 방식은 django1.7 미만 버전 방식입니다.
        이후 버전에서는 QuerySet을 구현한 다음 as_manager()로 Manager인스턴스를 생성해서 사용합니다.
    """

    def today(self) -> QuerySet:
        """
            오늘 주문
        :return:
        """
        today = date.today()
        day_start, day_end = (
            datetime.combine(today, datetime.min.time()),
            datetime.combine(today, datetime.max.time()),
        )

        return self.filter(created_at__range=(day_start, day_end))

    def not_complted(self, store: Store, store_id: int):
        """
            아직 완료되지 않은 주문
        :param store:
        :param store_id:
        :return:
        """
        # 해당하는 쿼리셋 작성
        ...


class OrderRawManger(models.Manager):
    def filter_by_blabla(self, blabla) -> list[Order]:
        """
            복잡한 쿼리로 데이터 조회
        """
        return self.raw(sql="""SELECT * FROM "ORDER" WHERE id < %s """, params=[blabla])


class Order(models.Model):

    objects = OrderQuerySet.as_manager()

    class Status(models.TextChoices):
        WAITING = "waiting", "주문 수락 대기중"
        ACCEPTED = "accepted", "주문 접수 완료"
        REJECTED = "rejected", "주문 거절"
        CANCEL = "cancel", "고객 취소"
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
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE)

    meta_info = models.OneToOneField(to="OrderMetaInfo", on_delete=models.CASCADE)

    objects = OrderQuerySet.as_manager()
    raw_objects = OrderRawManger()

    class Meta:
        db_table = "order"


class OrderMetaInfo(models.Model):
    """
        주문 관련 메타 정보들
    """

    use_coupon = models.BooleanField(default=False)
    use_cash = models.BooleanField(default=False)
    # 각종 메타 정보들 .....
    contract_product = models.ForeignKey(
        to="stores.ContractProduct",
        on_delete=models.PROTECT,
        help_text="주문이 접수된 시점에 상점이 사용중이던 계약상품",
    )

    class Meta:
        db_table = "order_meta_info"
