from __future__ import annotations

from typing import List, TYPE_CHECKING

from django.db import models


from datetime import date, datetime
from typing import Any

from django.db import connections
from django.db.models import QuerySet
from django.utils import timezone

if TYPE_CHECKING:
    from stores.models import Store


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


class PageableQuerySet(models.query.QuerySet):
    """
       활용 예제

       ```
           o_queryset = Order.objects.paging(strategy=Paging.CursorBased /* <-Enum임 */)
           o_list1 = o_queryset.next()
           o_list2 = o_queryset.next()
           o_list3 = o_queryset.next()
       ```

       이 페이징 QuerySet 메서드는 이렇게 만든 현재 코드도 꽤 쓸만한 방식이지만 제가 임시로 만든거라 아직 아쉽습니다.

       * Pagination 전략을 선택할수 있도록 QuerySet자체를 PaginationQuerySet을 만들어서
         상속 관계를 가지게하거나 args로 옵션을 받아서 아래와 같이 작성가능하도록 구현해도 좋습니다.

       나는 이를 경이로운 방법으로 구현했으나 코드에 여백이 부족해 적지 않는다.
    """

    _default_start_pk = -1
    _default_page_size = 10

    def pageable(self, start_pk=None) -> OrderQuerySet:
        """
            Cursor Based Pagination
        """
        s_pk = start_pk or self._default_start_pk
        return self.filter(id__gt=s_pk)

    def next(self, page_size=None) -> List[Order]:

        p_size = page_size or self._default_page_size
        paged_list = list(self.filter(id__gt=self._default_start_pk)[:p_size])
        if paged_list:
            self._default_start_pk = paged_list[-1].pk
        return paged_list


class OrderQuerySet(PageableQuerySet):


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
        :return:
        """
        return self.raw(sql="""SELECT * FROM "ORDER" WHERE id < %s """, params=[blabla])


class Order(models.Model):

    objects = OrderQuerySet.as_manager()


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
    created_at = models.DateTimeField(default=timezone.now)

    objects = OrderQuerySet.as_manager()
    raw_objects = OrderRawManger()

    class Meta:
        db_table = "order"
