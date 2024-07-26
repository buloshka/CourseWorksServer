import base64
import os
from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from ...models import Members, Users, Messages
from ...serializers import (UsersSerializer,
                            MemberSerializer,
                            MessagesSerializer)

from pathlib import Path

MAIN_DIR = str(Path(__file__).resolve().parent.parent.parent.parent)


def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            _, extension = os.path.splitext(image_path)
            return f"data:image/{extension[1:]};base64,{encoded_image}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None


class GetChatsMessagesAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        type_id = get_data('type_id')
        type_id = int(type_id) if type_id else 1
        user_id = int(get_data('user_id'))
        chat_id = int(get_data('chat_id'))
        other_id = int(get_data('other_id'))
        messages = []

        if type_id == 2:
            members = Members.objects.filter(chat_id=chat_id)
            all_parts_messages = [Messages.objects.filter(member=member) for member in members]
            for part in all_parts_messages:
                for message in part:
                    message_data = MessagesSerializer(message).data
                    date_string = message_data.get('created_date')
                    try:
                        datetime_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f+03:00')
                    except ValueError:
                        datetime_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S+03:00')
                    formatted_date = datetime_object.strftime('%d.%m.%Y %H:%M:%S.%f')
                    date, time = formatted_date.split(' ')
                    hhmm = time[:time.rfind(':'):]
                    message_data['created_date'] = ' '.join((date, hhmm))
                    user = message.member.user
                    user_data = UsersSerializer(user).data
                    partname = user.name + ' ' + user.surname
                    message_data['partname'] = partname
                    message_data['avatar'] = encode_image_to_base64(MAIN_DIR + user_data['avatar'])
                    messages.append(message_data)
        else:
            if other_id > -1:
                mines = Members.objects.filter(user_id=user_id)
                his = Members.objects.filter(user_id=other_id)
                all_mines = {member.chat for member in mines}
                all_his = {member.chat for member in his}
                chat = tuple(all_mines & all_his)[0]
                chat_id = chat.id

            users_members = Members.objects.filter(chat=chat_id)
            this_user = Users.objects.get(id=user_id)
            that_user = {member.user for member in users_members} ^ \
                        {this_user}
            that_user = UsersSerializer(tuple(that_user)[0]).data
            this_user = UsersSerializer(this_user).data

            first_messages = Messages.objects.filter(member=(
                MemberSerializer(Members.objects.get(
                    user_id=this_user['id'],
                    chat_id=chat_id)).data['id']
            ))
            second_messages = Messages.objects.filter(member=(
                MemberSerializer(Members.objects.get(
                    user_id=that_user['id'],
                    chat_id=chat_id)).data['id']
            ))

            for message in first_messages | second_messages:
                message_data = MessagesSerializer(message).data
                date_string = message_data.get('created_date')
                try:
                    datetime_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f+03:00')
                except ValueError:
                    datetime_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S+03:00')
                formatted_date = datetime_object.strftime('%d.%m.%Y %H:%M:%S.%f')
                date, time = formatted_date.split(' ')
                hhmm = time[:time.rfind(':'):]
                message_data['created_date'] = ' '.join((date, hhmm))
                messages.append(message_data)

        this_user = MemberSerializer(Members.objects.get(user_id=user_id, chat_id=chat_id)).data['id']

        return Response({
            'chat_id': chat_id,
            'user_id': user_id,
            'this_user': this_user,
            'messages': messages, },
            status=status.HTTP_200_OK)


class CreateMessageAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def put(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        member_id = int(get_data('member_id'))
        text = get_data('text')

        member = Members.objects.get(id=member_id)

        message = Messages.objects.create(member=member, text=text)
        message_data = MessagesSerializer(message).data

        return Response(data={'create': message_data}, status=status.HTTP_201_CREATED)


class EditMessageAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def patch(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        message_id = int(get_data('message_id'))
        text = get_data('text')

        message = Messages.objects.get(id=message_id)
        message.text = text
        message.save()

        message_data = MessagesSerializer(message).data

        return Response(data={'edit': message_data}, status=status.HTTP_200_OK)


class DeleteMessageAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def delete(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        message_id = int(get_data('message_id'))
        Messages.objects.get(id=message_id).delete()

        return Response(status=status.HTTP_200_OK)
