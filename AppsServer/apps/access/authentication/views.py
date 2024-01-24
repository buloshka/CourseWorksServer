from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from ...models import Users, Chats, Members
from ...serializers import UsersSerializer, UsersChatsSerializer

class SignInAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.query_params.get('email') or request.data.get('email')
        password = request.query_params.get('password') or request.data.get('password')

        data = try_to_get_user(email, password)
        if not data.get('signal'):
            return Response(**data.get('data'))

        user = data.get('data')
        user_data = UsersSerializer(user).data

        chats_data = {'chats': get_user_chats(user_data)}

        return Response(
            {'user': user_data,
             'chats': chats_data},
            status=status.HTTP_200_OK)


def try_to_get_user(email, password):
    try:
        user = Users.objects.get(email=email, password=password)
    except Exception as e:
        data = {
            'data': {'errors': 'Неверный логин или пароль.'},
            'status': status.HTTP_404_NOT_FOUND
        }
        return {'signal': False, 'data': data}
    return {'signal': True, 'data': user}


def get_user_chats(user):
    members = Members.objects.filter(user=user.get('id')).values()
    chats_ids = [member.get('chat_id') for member in members]

    if not chats_ids:
        return None

    chats = [Chats.objects.get(id=chat_id) for chat_id in chats_ids]
    data = [UsersChatsSerializer(chat).data for chat in chats]

    return data
