# Generated by Django 5.0.1 on 2024-03-06 08:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0014_alter_users_expiry_date_code_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='expiry_date_code',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 6, 8, 45, 57, 749660, tzinfo=datetime.timezone.utc)),
        ),
    ]
