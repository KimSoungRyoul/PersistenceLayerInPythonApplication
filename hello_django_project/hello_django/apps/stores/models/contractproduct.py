from django.db import models


class ContractProduct(models.Model):
    class ProductType(models.TextChoices):
        WELCOME = "welcome", "첫달 수수료 40% 할인 계약상품"
        NORMAL = "normal", "기본 계약상품"
        FRANCHISE = "franchise", "프렌차이즈업체 제휴계약상품"

    name = models.CharField(help_text="계약상품 이름", max_length=64)
    product_type = models.CharField(
        max_length=32,
        choices=ProductType.choices,
        default=ProductType.WELCOME,
        help_text="수수료 유형",
    )
    sales_commission = models.DecimalField(
        decimal_places=2, max_digits=5, help_text="판매 수수료(%)"
    )
