# Generated by Django 4.0.2 on 2022-04-30 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agents', '0010_alter_agentsusers_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentsusers',
            name='image',
            field=models.ImageField(default='default.img', upload_to='images'),
        ),
    ]
