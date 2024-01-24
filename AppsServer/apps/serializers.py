from rest_framework import serializers
from .authentication.models import Users, Chats
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
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance


class UsersChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = ('id', 'name', 'avatar')
