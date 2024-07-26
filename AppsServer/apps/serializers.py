from rest_framework import serializers
from .models import Users, Chats, Messages, Members, Subscriptions
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone
from datetime import timedelta

from secrets import choice


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['last_login', 'code', 'expiry_date_code']

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def is_code_expired(self, user):
        if user.expiry_date_code > timezone.now():
            return False
        return True

    def generate_code(self, user):
        if user.code and not self.is_code_expired(user):
            return user.code

        code = ''.join(choice('0123456789') for _ in range(6))

        try:
            Users.objects.get(code=code)
            self.generate_code(user)
        except Exception as e:
            user.code = code
            user.expiry_date_code = timezone.now() + timedelta(minutes=15)
            user.save()
            return code

    def clear_code(self, user):
        user.code = None
        user.save()

    def set_password(self, user, new_password):
        if self.is_code_expired(user):
            return False
        user.password = new_password
        user.save()
        self.clear_code(user)

        return True


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'


class UsersChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = ('id', 'name', 'avatar', 'type_id')


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ('id', 'member', 'text', 'created_date')


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = '__all__'
