# Generated by Django 5.0.1 on 2024-03-08 15:57

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0023_alter_users_expiry_date_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField()),
            ],
            options={
                'db_table': 'events',
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('chats', models.BooleanField()),
                ('media', models.BooleanField()),
                ('analytics', models.BooleanField()),
                ('themes', models.BooleanField()),
            ],
            options={
                'db_table': 'subscriptions',
            },
        ),
        migrations.AlterField(
            model_name='users',
            name='expiry_date_code',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 8, 16, 12, 6, 849903, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Eventhistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.users')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.events')),
            ],
            options={
                'db_table': 'eventhistory',
            },
        ),
        migrations.CreateModel(
            name='Purchasehistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.users')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.subscriptions')),
            ],
            options={
                'db_table': 'purchasehistory',
            },
        ),
    ]
