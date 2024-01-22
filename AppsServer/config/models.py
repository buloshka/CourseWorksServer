from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Users(AbstractBaseUser):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    fathername = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(unique=True, max_length=13)
    registration_date = models.DateTimeField()
    avatar = models.ImageField(upload_to='users/avatars', default='users/avatars/None.jpeg')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phonenumber']

    class Meta:
        app_label = 'config'
        db_table = 'users'


class Chattypes(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField()

    class Meta:
        app_label = 'config'
        db_table = 'chattypes'

'''
class Chats(models.Model):
    type_id = models.ForeignKey(Chattypes, models.DO_NOTHING)
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField()
    avatar = models.ImageField(upload_to='static/chats/avatars', default='static/chats/avatars/None.png')

    class Meta:
        app_label = 'config'
        db_table = 'chats'


class Roles(models.Model):
    chat_id = models.ForeignKey(Chats, models.DO_NOTHING)
    name = models.CharField(max_length=50)
    owner = models.BooleanField()
    admin = models.BooleanField()

    class Meta:
        app_label = 'config'
        db_table = 'roles'
        unique_together = (('id', 'chat_id'),)


class Members(models.Model):
    user_id = models.ForeignKey(Users, models.DO_NOTHING)
    chat_id = models.ForeignKey(Chats, models.DO_NOTHING)
    role_id = models.ForeignKey(Roles, models.DO_NOTHING)

    class Meta:
        app_label = 'config'
        db_table = 'members'
        unique_together = (('user_id', 'chat_id', 'role_id'),)


class Messages(models.Model):
    member_id = models.ForeignKey(Members, models.DO_NOTHING)
    text = models.TextField()
    created_date = models.DateTimeField()

    class Meta:
        app_label = 'config'
        db_table = 'messages'


class Logindetails(models.Model):
    user_id = models.ForeignKey(Users, models.DO_NOTHING)
    login = models.CharField(unique=True, max_length=100)
    password = models.CharField(unique=True, max_length=100)
    log_date = models.DateTimeField()

    class Meta:
        app_label = 'config'
        db_table = 'logindetails'


class Subscriptions(models.Model):
    name = models.CharField(unique=True, max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    chats = models.BooleanField()
    media = models.BooleanField()
    analytics = models.BooleanField()
    themes = models.BooleanField()

    class Meta:
        app_label = 'config'
        db_table = 'subscriptions'


class Purchasehistory(models.Model):
    user_id = models.ForeignKey(Users, models.DO_NOTHING)
    sub_id = models.ForeignKey(Subscriptions, models.DO_NOTHING)
    purchase_date = models.DateTimeField()

    class Meta:
        app_label = 'config'
        db_table = 'purchasehistory'


class Events(models.Model):
    description = models.CharField()

    class Meta:
        app_label = 'config'
        db_table = 'events'


class Eventhistory(models.Model):
    event_id = models.ForeignKey(Events, models.DO_NOTHING)
    user_id = models.ForeignKey(Users, models.DO_NOTHING)
    event_date = models.DateTimeField()

    class Meta:
        app_label = 'config'
        db_table = 'eventhistory'
'''
