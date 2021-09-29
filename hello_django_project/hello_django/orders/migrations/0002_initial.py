# Generated by Django 3.2.7 on 2021-09-29 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='product_set',
            field=models.ManyToManyField(through='orders.OrderedProduct', to='products.Product'),
        ),
    ]
