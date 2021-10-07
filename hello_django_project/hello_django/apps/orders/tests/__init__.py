from datetime import date, datetime, timedelta, timezone

from django.db.models import Q, QuerySet
from django.db.models import sql
from django.db.models.sql.datastructures import Join
from django.test import TestCase

from apps.orders.models import Order
from apps.stores.models import Contract, Store


# Create your tests here.


class QuerySetTest(TestCase):
    def setUp(self) -> None:
        store = Store.objects.create(name="시랑밥상")
        for i in range(1, 33):
            Order.objects.create(id=i, store=store)

    def test_use_queryset_not_manager(self):
        # infrastructure Layer를 그대로 노출시켜서 작성한 코드
        today = date.today()
        contract_queryset = (
            QuerySet(Contract)
            .select_related("store")
            .filter(start_date__gte=today, end_date__lt=today, store=1)
            .filter(end_date=today + timedelta(days=1))
        )
        list(contract_queryset)

        # 두 결과는 동일하다.
        # SELECT "stores_contract"."id",
        #        "stores_contract"."store_id",
        #        "stores_contract"."sales_commission",
        #        "stores_contract"."start_date",
        #        "stores_contract"."end_date"
        #   FROM "stores_contract"
        #  WHERE ("stores_contract"."end_date" < '2021-09-29'::date
        #       AND "stores_contract"."start_date" >= '2021-09-29'::date
        #       AND "stores_contract"."store_id" = 1
        #       AND "stores_contract"."end_date" = '2021-09-30'::date)

    def test_use_queryset_with_manager(self):
        # Manager(Domain Layer)를 사용해서 작성한 코드
        contract_queryset = Contract.objects.current_valid(store=1).tomorrow_expired()
        list(contract_queryset)
        # SELECT "stores_contract"."id",
        #        "stores_contract"."store_id",
        #        "stores_contract"."sales_commission",
        #        "stores_contract"."start_date",
        #        "stores_contract"."end_date"
        #   FROM "stores_contract"
        #  WHERE ("stores_contract"."end_date" < '2021-09-29'::date
        #       AND "stores_contract"."start_date" >= '2021-09-29'::date
        #       AND "stores_contract"."store_id" = 1
        #       AND "stores_contract"."end_date" = '2021-09-30'::date)

    def test_use_queryset_like_a_sqlalchemy(self):

        # infrastructure Layer를 그대로 노출시켜서 작성한 코드
        # 더 QuerySet이 아닌 Query로 작성
        today = date.today()

        query = sql.Query(model=Contract)
        query.add_q(Q(start_date__gte=today))
        query.add_q(Q(end_date__lt=today))
        query.add_q(Q(store=1))
        query.join(
            join=Join(
                table_name="store",
                parent_alias="stores_contract",
                join_type=sql.datastructures.INNER,
                join_field=Contract._meta.get_field("store"),
                table_alias=None,
                nullable=False,
            ),
        )
        print(query)
        # SELECT "stores_contract"."id", "stores_contract"."store_id", "stores_contract"."sales_commission", "stores_contract"."start_date",
        #          "stores_contract"."end_date"
        # FROM "stores_contract"
        # INNER JOIN "store" ON ("stores_contract"."store_id" = "store"."id")
        # WHERE ("stores_contract"."start_date" >= 2021-10-01 AND "stores_contract"."end_date" < 2021-10-01 AND "stores_contract"."store_id" = 1)

        print(query.sql_with_params())
        # ( "SELECT ... FROM WHERE ... < %s", (datetime.date(2021, 10, 1),)

        # Query()객체가 만들어준 sql은 이렇게 사용가능함
        # with connections["default"].cursor() as cursor:
        #     cursor.exetue(query.sql_with_params())
        #

    def test_no_pageable_queryset(self):
        """
            직접 페이징 처리 해주는 예제
        """
        # 직접 페이징 처리하는 예제
        today = timezone.now().today()
        day_start, day_end = (
            datetime.combine(today, datetime.min.time()),
            datetime.combine(today, datetime.max.time()),
        )
        o_query = Order.objects.filter(created_at__range=(day_start, day_end))

        order_list1: list[Order] = o_query.filter(id__gte=3)[:10]
        order_list2: list[Order] = o_query.filter(id__gte=order_list1[-1].id)[:10]
        order_list3: list[Order] = o_query.filter(id__gte=order_list2[-1].id)[:20]

        print(order_list1)
        print(order_list2)
        print(order_list3)


        Order.objects.filter(id=1)


        # [<Order: Order object (4)>, ... <Order: Order object (12)>, <Order: Order object (13)>]
        # [<Order: Order object (14)>, <Order: ... <Order: Order object (23)>]
        # [<Order: Order object (24)>, <Order: ... <Order: Order object (32)>]

    def test_pagination_queryset(self):
        """
            PageableQuerySet 사용 예제
            페이징 처리하는 코드가 매우 간결해졌다.
        """
        # PageableQuerySet 메서드 사용한 예제
        order_q = Order.objects.today().pageable(start_pk=3)

        order_list1: list[Order] = order_q.next()
        order_list2: list[Order] = order_q.next()
        order_list3: list[Order] = order_q.next(page_size=20)

        print(order_list1)
        print(order_list2)
        print(order_list3)

        # [<Order: Order object (4)>, ... <Order: Order object (12)>, <Order: Order object (13)>]
        # [<Order: Order object (14)>, <Order: ... <Order: Order object (23)>]
        # [<Order: Order object (24)>, <Order: ... <Order: Order object (32)>]




        (
            Order.objects
            .select_related("store__owner")
            .filter(store_id=1)
            .prefetch_related("orderedproduct_set")
         )

    #
    # def 왜_우리는_이런식으로_사용하는걸까_Model_objesct_블라블라(self):
    #
    #     Order.objects.filter(...)
    #     Store.objects.filter(...)
    #     Contract.objects.filter(...)
    #
    #      order_queryset = QuerySet(Order).filter().select_related()...
    #         store_queryset = QuerySet(Store).filter().select_related()...
    #         contract_queyset = QuerySet(Contract).filter().select_related()...

