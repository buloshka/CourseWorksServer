from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from django.utils import timezone
from datetime import timedelta


class UserManager(models.Manager):
    pass


class Users(AbstractBaseUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    fathername = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=345)
    phonenumber = models.CharField(unique=True, max_length=15)
    registration_date = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='static/users/avatars',
                               default='static/users/avatars/None.png',
                               null=True)
    code = models.CharField(unique=True, max_length=6, null=True)
    expiry_date_code = models.DateTimeField(default=timezone.now() + timedelta(minutes=15))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phonenumber']

    class Meta:
        app_label = 'config'
        db_table = 'users'


class Chattypes(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        app_label = 'config'
        db_table = 'chattypes'


class Chats(models.Model):
    type = models.ForeignKey(Chattypes, models.DO_NOTHING, default=1)
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='static/chats/avatars', default='static/chats/avatars/None.png', null=True, blank=True)

    objects = models.Manager()

    class Meta:
        app_label = 'config'
        db_table = 'chats'


class Roles(models.Model):
    chat = models.ForeignKey(Chats, models.DO_NOTHING, null=True)
    name = models.CharField(max_length=50)
    owner = models.BooleanField()
    admin = models.BooleanField()

    objects = models.Manager()

    class Meta:
        app_label = 'config'
        db_table = 'roles'
        unique_together = (('id', 'chat'),)


class Members(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    chat = models.ForeignKey(Chats, models.DO_NOTHING)
    role = models.ForeignKey(Roles, models.DO_NOTHING, default=1)

    objects = models.Manager()

    class Meta:
        app_label = 'config'
        db_table = 'members'
        unique_together = (('user', 'chat', 'role'),)


class Messages(models.Model):
    member = models.ForeignKey(Members, models.DO_NOTHING)
    text = models.TextField(max_length=10000)
    created_date = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()

    class Meta:
        app_label = 'config'
        db_table = 'messages'


class Subscriptions(models.Model):
    name = models.CharField(unique=True, max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    chats = models.BooleanField()
    media = models.BooleanField()
    analytics = models.BooleanField()
    themes = models.BooleanField()
    
    objects = models.Manager()

    class Meta:
        app_label = 'config'
        db_table = 'subscriptions'


class Purchasehistory(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    sub = models.ForeignKey(Subscriptions, models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()

    class Meta:
        app_label = 'config'
        db_table = 'purchasehistory'


class Events(models.Model):
    description = models.CharField(max_length=100)
    
    objects = models.Manager()

    class Meta:
        app_label = 'config'
        db_table = 'events'


class Eventhistory(models.Model):
    event = models.ForeignKey(Events, models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    event_date = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()

    class Meta:
        app_label = 'config'
        db_table = 'eventhistory'
