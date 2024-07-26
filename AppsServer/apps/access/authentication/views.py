from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from ...models import Users, Chats, Members, Events, Eventhistory
from ...serializers import UsersSerializer, UsersChatsSerializer


class SignInAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.query_params.get('login') or request.data.get('login')
        password = request.query_params.get('password') or request.data.get('password')

        data = try_to_get_user(email, password)
        if not data.get('signal'):
            return Response(**data.get('data'))

        user = data.get('data')
        user_data = UsersSerializer(user).data

        chats_data = {'chats': get_user_chats(user_data)}

        event = Events.objects.get(description='Sign in')
        Eventhistory.objects.create(
            event=event,
            user=user,
        )

        return Response(
            {'user': user_data,
             'chats': chats_data},
            status=status.HTTP_200_OK)


def try_to_get_user(login, password):
    try:
        user = Users.objects.get(email=login, password=password)
        return {'signal': True, 'data': user}
    except Exception as e:
        try:
            user = Users.objects.get(phonenumber=login, password=password)
            return {'signal': True, 'data': user}
        except Exception as e:
            data = {
                'data': {'errors': 'Invalid login or password'},
                'status': status.HTTP_404_NOT_FOUND
            }
            return {'signal': False, 'data': data}


def get_user_chats(user):
    members = Members.objects.filter(user=user.get('id')).values()
    chats_ids = [member.get('chat_id') for member in members]

    if not chats_ids:
        return None

    chats = [Chats.objects.get(id=chat_id) for chat_id in chats_ids]
    data = [UsersChatsSerializer(chat).data for chat in chats]

    return data
