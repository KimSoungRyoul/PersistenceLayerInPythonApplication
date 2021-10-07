from datetime import date, timedelta

from django.db import transaction
from django.test import TestCase

from apps.users.models import User
from infrastructure.models.exceptions import DomainException
from apps.stores.models import Contract, ContractProduct, Store

from apps.stores.models.utils import StoreUtil

# 도메인서비스를 행하는 주체 "StoreUtil(store)"가 존재한다.
# StoreUtil이라는 도메인서비스는
# 1. 복잡한 도메인로직을 특정 애그리거트(Root Model)로 부터 책임을 분리하는 역할을하며
# 2. "주체"가 XXX라는 행위를 한다.이때 필요한 애그리거트들은 args다. 라는 도메인로직을 표현하는 DDD설계 도구로서 활용된다.


class StoreDomainTestCase(TestCase):
    """
        도메인서비스 TestCase는 개발문서 역할을 담당한다.

        복잡한 도메인로직을 문서화하는 것은 시간이 항상 부족하다.
        또한 문서는 시간이 지나면 달라지는 도메인로직으로 인해 쓸모없어진다.

        도메인서비스를 구현하고 이에 관련된 TestCase를 작성하게되면
        이는 실시간으로 최신화는 개발문서로서 활용될수있다.

    """

    def setUp(self) -> None:
        ContractProduct.objects.create(
            name="첫 가입 수수료 할인상품",
            product_type=ContractProduct.ProductType.WELCOME,
            sales_commission=5.00,
        )

    def test_store_contract(self):
        store = Store.objects.create(name="김차도가")
        contract_product = ContractProduct.objects.get(name="첫 가입 수수료 할인상품")

        contract = StoreUtil(store).sign_contract(
            contract_product=contract_product,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
        )

        assert contract

    def test_store_contract_fail_caused_by_valid_contract_exists(self):
        store = Store.objects.create(name="김차도가")
        contract_product = ContractProduct.objects.get(name="첫 가입 수수료 할인상품")
        Contract.objects.create(
            store=store,
            contract_product=contract_product,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
        )

        # Expected : 이미 유효한 계약이 존재하면 DomainExcpetion을 raise한다.
        with self.assertRaises(DomainException):
            StoreUtil(store).sign_contract(
                contract_product=contract_product,
                start_date=date.today() - timedelta(days=1),
                end_date=date.today() + timedelta(days=1),
            )

    def test_what_is_manager(self):
        from django.db.models import Manager, QuerySet


        self.assertTrue(isinstance(User.objects, Manager))
        self.assertTrue(isinstance(User.objects.filter(id=1), QuerySet))



    def test_asdf(self):

        # Database transaction Manage만으로도 비즈니스 로직이 제어가능하다면 굳이 Service계층이 필요한가?
        with transaction.atomic():
            store = Store.objects.create(...)
            contract =Contract.objects.create(...)

            ...