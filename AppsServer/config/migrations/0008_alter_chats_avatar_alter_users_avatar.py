# Generated by Django 5.0.1 on 2024-01-24 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0007_alter_roles_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='avatar',
            field=models.ImageField(blank=True, default='static/chats/avatars/None.png', null=True, upload_to='static/chats/avatars'),
        ),
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.ImageField(blank=True, default='static/users/avatars/None.png', null=True, upload_to='static/users/avatars'),
        ),
    ]
