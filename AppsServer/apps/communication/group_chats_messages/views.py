from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from ...models import Members, Users, Messages, Chats
from ...serializers import (UsersSerializer,
                            MemberSerializer,
                            MessagesSerializer)


class CreateGroupAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def put(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        user_id = int(get_data('user_id'))
        title = get_data('title')
        image = get_data('image')
        users = [int(user) for user in get_data('users').split()]
        members = []

        if image:
            chat = Chats.objects.create(name=title, type_id=2, avatar=image)
        else:
            chat = Chats.objects.create(name=title, type_id=2)

        Members.objects.create(user_id=user_id, chat=chat, role_id=2)
        for member_id in users:
            user = Users.objects.get(id=member_id)
            member = Members(user=user, chat=chat, role_id=3)
            members.append(member)

        Members.objects.bulk_create(members)

        return Response(
            data={'chat_id': chat.id},
            status=status.HTTP_201_CREATED
        )
