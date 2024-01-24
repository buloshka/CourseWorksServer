from rest_framework import serializers
from .models import Users, Chats
from rest_framework_simplejwt.tokens import RefreshToken


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['last_login']

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


class UsersChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = ('id', 'name', 'avatar')
