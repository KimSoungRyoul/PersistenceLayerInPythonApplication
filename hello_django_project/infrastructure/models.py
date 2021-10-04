from typing import Generic, TypeVar

from django.db.models import Model

ModelType = TypeVar("Model", bound=Model)


class DomainUtil(Generic[ModelType]):
    """
        도메인 서비스: 애그리거트(Aggregate)간 연산 작업이 필요한 경우 이곳에 구현한다.

        ex: "주문 쿠폰 할인 결제금액 계산" 이라는 도메인 로직은 어디에 구현되어야하는가?
            Model이 Order, Coupon, Payment가 존재한다고 가정을하면

            ```
            class Order(models.Model):
                ...

                def calculate_discount_price(self, payment:Payment, coupon:Coupon):
                    from models import Coupon, Payment

                    # 할인 계산 로직....
            ```

        이런식으로 구현이 될텐데 이렇게 되면 Order라는 Model에 너무 과도한 책임이 주어진다.
        Order Model 내부에는 Order을 계산하는 도메인 로직만 존재해야하고
        다른 도메인들과 연계되어서 동작하는 로직들은 "Domain Service"라는 모듈에서 책임지도록 한다.
    """

    def __init__(self, instance: ModelType):
        self.instance = instance
