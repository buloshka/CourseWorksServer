# Generated by Django 5.0.1 on 2024-03-07 08:30

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0021_alter_users_expiry_date_code_delete_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='expiry_date_code',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 7, 8, 45, 10, 332317, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.members')),
            ],
            options={
                'db_table': 'messages',
            },
        ),
    ]