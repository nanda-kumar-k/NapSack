# Generated by Django 4.0.2 on 2022-04-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dealer', '0002_dealerorders_dealer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealertlocation',
            name='latitude',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='dealertlocation',
            name='longitude',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
