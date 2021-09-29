# Generated by Django 3.2.7 on 2021-09-29 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', '주문 수락 대기중'), ('accepted', '주문 접수 완료'), ('rejected', '주문 거절'), ('delivery complete', '배달 완료')], default='waiting', help_text='주문 상태값', max_length=32)),
                ('total_price', models.IntegerField(default=0)),
                ('address', models.CharField(help_text='주문 배송지', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, help_text='주문한 해당 메뉴의 갯수')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
            options={
                'db_table': 'ordered_product',
            },
        ),
    ]