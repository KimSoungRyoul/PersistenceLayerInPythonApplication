from datetime import date

from hello_django_project.infrastructure.models import DomainUtil
from stores.models import Contract, ContractProduct, Store
from stores.models.exceptions import DomainException


class StoreUtil(DomainUtil[Store]):
    """
           Contract DomainService

           여러 Model이 함께 동작한다 하도라도 "주어"에 해당하는 Model이 존재한다.
           ex:
               * "상점(Store)"이 "계약"(Contract)을 체결하다.
    """

    def sign_contract(
        self, contract_product: ContractProduct, start_date: date, end_date: date,
    ) -> Contract:
        # 계약은 체결하기전 수행하는 검토는 복잡할수 있다.
        # 여기서는 간결하게 예시만 보여준다.
        if self.instance.contract_set.current_valid().exists():
            raise DomainException(detail="이미 사용중인 계약이 존재합니다.")

        return Contract.objects.create(
            store=self.instance,
            contract_product=contract_product,
            start_date=start_date,
            end_date=end_date,
        )


class ContractUtil(DomainUtil[Contract]):
    """
        Contract DomainService

    """

    ...
