# Generated by Django 5.0.1 on 2024-03-06 09:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0016_alter_users_email_alter_users_expiry_date_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='code',
            field=models.CharField(max_length=6, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='expiry_date_code',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 6, 9, 26, 33, 12665, tzinfo=datetime.timezone.utc)),
        ),
    ]
