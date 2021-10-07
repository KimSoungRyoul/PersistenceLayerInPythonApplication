from logging import log
from typing import Callable

from rest_framework.exceptions import APIException

from app.models import User
from apps.orders.models.utils import OrderUtil, PayDTO, PayRes
from apps.orders.tests.models.test_order import request_shinhan_card
from apps.stores.models import Store
from django.db import transaction

from infrastructure.models.exceptions import DomainException


def refund_payment_func():
    pass


def send_event_to_subscriber_microservice():
    pass


class EventFailExcepation(Exception):
    pass


def request_api_to_microservice():
    pass


def send_push_msg_to_store(msg_type):
    pass


class PushException:
    pass


from django_mysql.exceptions import TimeoutError
from django_mysql.locks import Lock

from redis import Redis
conn = Redis()

import redis_lock
from django.core.cache import cache

class Coupon:
    pass


class CouponService:

    def provide_coupon(self, user:User):
        # 쿠폰 갯수를 카운트하는 키값을 아무도 점유하지 못하게 Lock을 건다.
        with cache.lock("current_issued_coupon_count"):
            cnt = cache.get("current_issued_coupon_count")
            # 20_000개보다 적으면 쿠폰생성하고 redis 키값을 increase 하고 자원 해제
            if cnt <=20_000:
                # 도메인 로직이 단순하면 DomainService로직 구현 생략
                Coupon.objects.create(user=user)
                cache.incr("current_issued_coupon_count")


class Review:
    pass


class ReviewAPIRequest:
    pass


class StoreService:

    def retrieve_store_detail(self,pk)->Store:
        store = Store.objects.get(pk=pk)

        try:
            review_list:list[Review] = ReviewAPIRequest.request_reviews(store_id=pk, timeout=1)
        except APIException as e :
            review_list = []

        store.review_list = review_list

        return store





class OrderService:





    @transaction.atomic
    def take_order(self, store_id, user: User, *args):
        """
            주문 접수 Service
        """
        store = Store.objects.get(id=store_id)

        # 결제 모듈을 어떤것을 사용할것인지는 여기서 결정한다.
        # 여기는 간소화한 분기절이지만 결제는 여러가지 모듈이 존재하고(XXX페이, 신용카드, 포인트사용 ...)
        # 실무에서는 이것을 추상화하는 모듈이 따로 구현되어있어야 한다.
        if ...:
            payment_func: Callable[[PayDTO], PayRes] = request_shinhan_card

        # 주문 데이터 생성과 함께 결제 시도
        try:
            order = OrderUtil().take_a_order(store=store, user=user, payment_function=payment_func)
        except DomainException as e:
            # 주문 접수 생성 실패로 인해 결제 취소로직이 수행되어야한다.
            refund_payment_func()
            raise e

        try:
            # 이벤트를 발송하는 로직은 InfraStructure로직이고
            # 이런식으로 Service로직에 노출되는 것보다 도메인 로직 Action들 사이에 hooking되는 것이 좀더 바람직하다.
            # 이러한 아쉬운 점들은 지금은 그냥 넘어가자
            send_event_to_subscriber_microservice(...)
        except EventFailExcepation as e: # DomainExcepation처럼 인프라 모듈에 선언된 커스텀 익셉션
            # 이벤트를 전달하는 솔루션에 장애가 생긴다면 (ex: AWS 전면장애)
            # api Call로 직접 전달한다.
            request_api_to_microservice(event_type="create",...)
            raise e

        # 푸시메시지 전송은 rollback이 불가능하기때문에 가장 마지막에 수행한다.
        try:
            send_push_msg_to_store(msg_type="kakao_alimtalk")
        except PushException as e:
            request_api_to_microservice(event_type="delete", ...)
            refund_payment_func()
            raise e
