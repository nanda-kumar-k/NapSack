# Generated by Django 4.0.2 on 2022-04-29 11:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Dealer', '0007_remove_dealershopsverifications_agent_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealershopsverifications',
            name='verification_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
