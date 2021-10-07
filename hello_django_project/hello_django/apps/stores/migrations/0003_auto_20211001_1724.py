# Generated by Django 3.2.7 on 2021-10-01 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='계약상품 이름', max_length=64)),
                ('product_type', models.CharField(choices=[('welcome', '첫달 수수료 40% 할인 계약상품'), ('normal', '기본 계약상품'), ('franchise', '프렌차이즈업체 제휴계약상품')], default='welcome', help_text='수수료 유형', max_length=32)),
                ('sales_commission', models.DecimalField(decimal_places=2, help_text='판매 수수료(%)', max_digits=5)),
            ],
        ),
        migrations.RemoveField(
            model_name='contract',
            name='sales_commission',
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_product',
            field=models.ForeignKey(default=1, help_text='계약삼품(수수료를 결정한다)', on_delete=django.db.models.deletion.RESTRICT, to='stores.contractproduct'),
            preserve_default=False,
        ),
    ]