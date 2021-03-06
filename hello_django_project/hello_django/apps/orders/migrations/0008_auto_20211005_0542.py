# Generated by Django 3.2.7 on 2021-10-05 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_businesshour'),
        ('orders', '0007_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('waiting', '주문 수락 대기중'), ('accepted', '주문 접수 완료'), ('rejected', '주문 거절'), ('cancel', '고객 취소'), ('delivery complete', '배달 완료')], default='waiting', help_text='주문 상태값', max_length=32),
        ),
        migrations.CreateModel(
            name='OrderMetaInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_coupon', models.BooleanField(default=False)),
                ('use_cash', models.BooleanField(default=False)),
                ('contract_product', models.ForeignKey(help_text='주문이 접수된 시점에 상점이 사용중이던 계약상품', on_delete=django.db.models.deletion.PROTECT, to='stores.contractproduct')),
            ],
            options={
                'db_table': 'order_meta_info',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='meta_info',
            field=models.OneToOneField(default=-1, on_delete=django.db.models.deletion.CASCADE, to='orders.ordermetainfo'),
            preserve_default=False,
        ),
    ]
