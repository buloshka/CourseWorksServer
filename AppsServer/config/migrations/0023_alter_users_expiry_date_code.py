# Generated by Django 5.0.1 on 2024-03-07 09:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0022_alter_users_expiry_date_code_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='expiry_date_code',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 9, 28, 6, 6307, tzinfo=datetime.timezone.utc)),
        ),
    ]