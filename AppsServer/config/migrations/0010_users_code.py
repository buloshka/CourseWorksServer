# Generated by Django 5.0.1 on 2024-02-01 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0009_alter_users_registration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='code',
            field=models.CharField(max_length=8, null=True),
        ),
    ]