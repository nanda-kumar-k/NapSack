# Generated by Django 4.0.2 on 2022-05-12 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0010_customerusers_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerusers',
            name='image',
        ),
        migrations.CreateModel(
            name='CustomerImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='customer_images/default_profile_img.png', upload_to='customer_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Customer.customerusers')),
            ],
        ),
    ]
