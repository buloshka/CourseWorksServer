# Generated by Django 5.0.1 on 2024-01-24 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0005_alter_chats_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='config.roles'),
        ),
    ]
