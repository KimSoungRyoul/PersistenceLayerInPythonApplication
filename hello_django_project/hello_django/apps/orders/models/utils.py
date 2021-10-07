from __future__ import annotations

from typing import Callable, TypeVar

from app.models import User
from infrastructure.models.exceptions import DomainException
from infrastructure.models.utils import DomainUtil
from apps.orders.models import Order
from apps.stores.models import Store

PayRes = TypeVar("PayResponse", bound=str)
PayDTO = TypeVar("PayDTO", bound=object)

PushNotiRes = TypeVar("PushNotiRes", bound=str)
PushNotiDTO = TypeVar("PushNotiDTO", bound=object)


class OrderUtil(DomainUtil[Order]):
    """
       DomainService: 주문
    """

    def take_a_order(
        self,
        store: Store,
        user: User,
        paydto: PayDTO,
        payment_function: Callable[[PayDTO], PayRes],
    ) -> Order:
        """
            주문 접수
        """
        if not store.is_open():
            raise DomainException(detail="이미 영업이 종료된 상점입니다.")

        order = Order.objects.create_order(store=store, user=user)

        if order.ordermetainfo.use_cash:
            # 현금 결제인경우 결제모듈 수행 스킵
            return order

        if (pay_res := payment_function(paydto)) and "잔액부족" in pay_res:
            raise DomainException(detail=f"결제 실패, 상세사유: {pay_res}")

        self.instance = order
        return self.instance

    def accept_a_order(
        self,
        store: Store,
        push_dto: PushNotiDTO,
        push_noti_function: Callable[[PushNotiDTO], PushNotiRes],
    ) -> Order:
        """
            주문 수락
        """
        if self.instance.status == Order.Status.CANCEL:
            raise DomainException(detail="이미 고객이 취소한 주문입니다.")

        self.instance.status = Order.Status.ACCEPTED
        # 각 종 주문정보 변경
        # 배달 예상시간,  쿠폰 사용한경우 쿠폰 사용완료처리
        self.instance.save()

        # 비동기로 던지면 더욱 좋다.
        push_noti_function(push_dto)

        return self.instance

    def reject_a_order(self, *args) -> Order:
        """
            주문 취소
        :return:
        """
        ...
        return self.instance


