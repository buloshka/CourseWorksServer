# Generated by Django 5.0.1 on 2024-01-24 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0006_alter_members_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roles',
            name='chat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='config.chats'),
        ),
    ]
