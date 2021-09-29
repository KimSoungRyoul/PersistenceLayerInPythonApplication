from datetime import date, timedelta

from django.db.models import QuerySet

# Create your views here.
from stores.models import Contract


def use_queryset_like_a_sqlalchemy():
    today = date.today()
    contract_queryset = QuerySet(Contract).filter(start_date__gte=today, end_date__lt=today, store=1).filter(end_date=today + timedelta(days=1))
    list(contract_queryset)

    contract_queryset = Contract.objects.current_valid(store=1).tomorrow_expired()
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
