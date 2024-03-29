# Generated by Django 5.0.1 on 2024-01-24 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_roles_members'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chats',
            old_name='type_id',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='members',
            old_name='chat_id',
            new_name='chat',
        ),
        migrations.RenameField(
            model_name='members',
            old_name='role_id',
            new_name='role',
        ),
        migrations.RenameField(
            model_name='members',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='roles',
            old_name='chat_id',
            new_name='chat',
        ),
        migrations.AlterUniqueTogether(
            name='members',
            unique_together={('user', 'chat', 'role')},
        ),
        migrations.AlterUniqueTogether(
            name='roles',
            unique_together={('id', 'chat')},
        ),
    ]
