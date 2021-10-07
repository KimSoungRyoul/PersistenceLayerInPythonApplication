from collections import Callable
from unittest.mock import MagicMock

from django.test import TestCase
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.orders.models import Order
from apps.orders.models.utils import OrderUtil
from apps.stores.models import Store
from apps.users.models import User


def request_shinhan_card(*args):
    # 신한카드 결제 모듈
    return ""


def request_notification(*args):
    #  카카오 알림톡 전송
    return ""


class OrderDomainTestCase(TestCase):
    def test_take_order(self):
        store = Store.objects.get(id=1)
        user = User.objects.get(id=1)

        # 도메인 로직을 테스트하기위해서 결제 모듈이 모킹하는 방식이 쉬워진다.
        payment_func: Callable = MagicMock()

        OrderUtil().take_a_order(store=store, user=user, payment_function=payment_func)


from rest_framework.viewsets import GenericViewSet


class OrderViewSet(GenericViewSet):
    def create(self, request: Request):

        store = Store.objects.get(id=request.data["store_id"])
        user = User.objects.get(id=request.user.id)

        # 결제 모듈을 어떤것을 사용할것인지는 여기서 결정한다.
        # 여기는 간소화한 분기절이지만 결제는 여러가지 모듈이 존재하고(XXX페이, 신용카드, 포인트사용 ...)
        # 실무에서는 이것을 추상화하는 모듈이 따로 구현되어있어야 한다.
        if ...:
            payment_func: Callable = request_shinhan_card

        OrderUtil().take_a_order(store=store, user=user, payment_function=payment_func)

        return Response(data={"detail": "주문 접수가 완료되었습니다."})

    @action(
        detail=True, url_path="accept",
    )
    def accept(self, request: Request, pk):

        instance: Order = self.get_object()
        store = Store.objects.get(id=request.data["store_id"])

        # 푸시 알림 모듈을 어떤것을 사용할것인지는 여기서 결정한다.
        # 여기는 간소화한 분기절이지만 푸쉬노티는 여러가지 모듈이 존재하고(카카오 모바일자체푸쉬, SMS...)
        # 실무에서는 이것을 추상화하는 모듈이 따로 구현되어있어야 한다.
        if ...:
            push_noti_func: Callable = request_notification

        OrderUtil(instance).accept_a_order(
            store=store, push_noti_function=push_noti_func
        )

        return Response(data={"detail": "주문이 수락되었습니다."})
