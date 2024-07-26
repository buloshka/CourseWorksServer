import os
import base64
from PIL import Image, ImageDraw

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from ...models import Members, Chats, Roles, Users, Messages
from ...serializers import (UsersChatsSerializer,
                            UsersSerializer)

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


def decode_base64_to_image(encoded_data, save_path):
    try:
        _, data = encoded_data.split(',', 1)
        decoded_image = base64.b64decode(data)
        with open(save_path, "wb") as image_file:
            image_file.write(decoded_image)
    except Exception as e:
        print(f"Error decoding image: {e}")


def round_image(path, filename):
    image = Image.open(path + filename)

    width, height = image.size
    diameter = min(width, height)

    rounded_image = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(rounded_image)

    draw.ellipse([(0, 0), (diameter, diameter)], fill=(255, 255, 255, 255))
    rounded_image.paste(image.resize((diameter, diameter)), (0, 0), mask=rounded_image)

    point = filename.rfind('.')
    new_filename = filename[:point:]
    rounded_filename = path + "Circled_" + new_filename + '.png'
    rounded_image.save(rounded_filename, format="PNG")

    data = encode_image_to_base64(rounded_filename)
    os.remove(rounded_filename)

    return data


class GetAllChatsAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        user_id = int(get_data('user_id'))

        chats = []
        exclude_users = []

        users = Users.objects.exclude(id=user_id)
        members = Members.objects.filter(user_id=user_id)
        for member in members:
            chat = member.chat
            other_user = Members.objects.filter(chat=chat).exclude(user_id=user_id)
            if len(other_user) > 0:
                other_user = other_user[0].user
                exclude_users.append(other_user)

        for user in set(exclude_users) ^ set(users):
            user_data = UsersSerializer(user).data

            avatar = user_data['avatar']
            point = avatar.rfind('/') + 1
            filename = avatar[point::]
            path = MAIN_DIR + avatar[:point:]

            picture = round_image(path, filename)
            fathername = user_data.get('fathername')
            user_data['name'] = ' '.join([
                user_data.get('surname'),
                user_data.get('name'),
                fathername if fathername else '',
            ]).strip()
            user_data['avatar'] = picture
            user_data['that_id'] = user_data.get('id')

            user_data.pop('surname')
            user_data.pop('fathername')
            user_data.pop('token')
            user_data.pop('email')
            user_data.pop('phonenumber')
            user_data.pop('registration_date')
            chats.append(user_data)

        return Response(
            {'chats': chats},
            status=status.HTTP_200_OK)


class GetChatsAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        user_id = int(get_data('user_id'))
        is_for_group = bool(get_data('group'))
        chats = []

        try:
            this_members = Members.objects.filter(user=user_id)
        except Exception as e:
            return Response({'chats': []}, status=status.HTTP_200_OK)

        for this_member in this_members:
            chat = this_member.chat
            chat_data = UsersChatsSerializer(chat).data
            if is_for_group and chat.type.name == 'Групповые чаты':
                continue
            elif chat.type.name == 'Групповые чаты':
                avatar = chat_data['avatar']
                point = avatar.rfind('/') + 1
                filename = avatar[point::]
                path = MAIN_DIR + avatar[:point:]
                chat_data['avatar'] = round_image(path, filename)
                chat_data['that_id'] = -1
                chat_data['is_owner'] = this_member.role.owner
                chats.append(chat_data)
                continue

            users_members = Members.objects.filter(chat=chat.id)
            that_members = {member.user for member in users_members} ^ \
                           {Users.objects.get(id=user_id)}

            for that_member in that_members:
                that_member = UsersSerializer(that_member).data

                avatar = that_member['avatar']
                point = avatar.rfind('/') + 1
                filename = avatar[point::]
                path = MAIN_DIR + avatar[:point:]

                picture = round_image(path, filename)
                fathername = that_member.get('fathername')
                chat_data['name'] = ' '.join([
                    that_member.get('surname'),
                    that_member.get('name'),
                    fathername if fathername else '',
                ]).strip()
                chat_data['avatar'] = picture
                chat_data['that_id'] = that_member.get('id')
                chat_data['is_owner'] = True
                chats.append(chat_data)

        return Response(
            {'chats': chats},
            status=status.HTTP_200_OK)


class GetChatAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        user_id = int(get_data('user_id'))
        chat_id = int(get_data('chat_id'))
        chats = []

        chat = UsersChatsSerializer(Chats.objects.get(id=chat_id))
        chat_data = chat.data

        users_members = Members.objects.filter(chat=chat_id)
        this_user = Users.objects.get(id=user_id)
        that_user = {member.user for member in users_members} ^ \
                      {this_user}
        that_user = UsersSerializer(tuple(that_user)[0]).data

        avatar = that_user['avatar']
        point = avatar.rfind('/') + 1
        filename = avatar[point::]
        path = MAIN_DIR + avatar[:point:]

        picture = round_image(path, filename)
        fathername = that_user.get('fathername')
        chat_data['name'] = ' '.join([
            that_user.get('surname'),
            that_user.get('name'),
            fathername if fathername else '',
        ]).strip()
        chat_data['avatar'] = picture
        chat_data['that_id'] = that_user.get('id')
        chats.append(chat_data)

        return Response(
            {'chat': chats},
            status=status.HTTP_200_OK)


class CreateSingleChatAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def put(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        this_user_id = int(get_data('this_user_id'))
        that_user_id = int(get_data('that_user_id'))

        this_user = Users.objects.get(id=this_user_id)
        that_user = Users.objects.get(id=that_user_id)

        chat = Chats.objects.create(name=f'{this_user.id}_{that_user.id}')
        Members.objects.bulk_create([
            Members(user=this_user, chat=chat),
            Members(user=that_user, chat=chat),
        ])

        return Response(status=status.HTTP_201_CREATED)


class DeleteChatAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def delete(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        chat_id = int(get_data('chat_id'))
        members = Members.objects.filter(chat=chat_id)

        messages = []
        for member in members:
            for message in Messages.objects.filter(member=member):
                messages.append(message)

        roles = Roles.objects.filter(chat=chat_id)
        chat = Chats.objects.get(id=chat_id)

        for message in messages: message.delete()
        roles.delete()
        members.delete()
        chat.delete()

        return Response(status=status.HTTP_200_OK)
