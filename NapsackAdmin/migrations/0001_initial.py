# Generated by Django 4.0.2 on 2022-04-26 11:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllPayments',
            fields=[
                ('nap_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_id', models.CharField(max_length=200)),
                ('payment_status', models.CharField(max_length=100)),
                ('payment_request_id', models.CharField(max_length=200)),
                ('user_id', models.UUIDField()),
                ('amount_paid', models.CharField(max_length=200)),
                ('on_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ShopsCategories',
            fields=[
                ('Shops_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProductsCategories',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('categories_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NapsackAdmin.shopscategories')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('specifications', models.TextField()),
                ('descriptions', models.TextField()),
                ('image', models.ImageField(upload_to='images')),
                ('categories_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NapsackAdmin.productscategories')),
            ],
        ),
    ]
