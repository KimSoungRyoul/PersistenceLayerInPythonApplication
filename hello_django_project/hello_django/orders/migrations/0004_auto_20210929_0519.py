# Generated by Django 3.2.7 on 2021-09-29 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyOrderReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_order_cnt', models.IntegerField()),
                ('hours_chicken_cnt', models.IntegerField()),
                ('hours_order_cnt_with_coupon', models.IntegerField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrderReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_order_cnt', models.IntegerField()),
                ('weekly_order_cnt', models.IntegerField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
    ]