from datetime import date

from django.core.management.base import BaseCommand

from orders.models import DailyOrderReport, Order


class Command(BaseCommand):
    help = "주문 통계 보고서 뽑아주는 커맨드"

    def add_arguments(self, parser):
        parser.add_argument(
            "--type", action="store", required=False, help="통계 자료 보고방식", default="log",
        )

    def handle(self, *args, **options):
        send_type = options["type"]

        daily_report: DailyOrderReport = Order.raw_objects.get_daily_report(
            day=date.today()
        )

        if send_type == "log":
            self.stdout.write(self.style.SUCCESS(str(daily_report)))
        elif send_type == "slack":
            ...
        elif send_type == "email":
            ...
        ...




        # 이런식으로 sql이 프로젝트내 Layer 구분없이 노출되어있는 코드들은 아키텍처 측면에서 보면 안티 패턴이다.
        Order.objects.raw(sql = """
        SELECT * FROM "ORDER" 블라블라 
        """)

        # Manager 클래스를 적극 활용하면 코드를 읽는 개발자입장에서는 ORM과 차이없게 만들수 있다.
        # Manager에게 Persistence Layer의 책임을 확실하게 위임함
        Order.raw_objects.filter(blabla=".....").prefetch_related("....")