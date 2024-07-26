from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from ...models import Users, Events, Eventhistory
from ...serializers import UsersSerializer


class SignUpAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        def get_data(name):
            return request.data.get(name) or request.query_params.get(name)

        validated_data = {}
        params = {
            'name': get_data('name'),
            'surname': get_data('surname'),
            'fathername': get_data('fathername'),
            'phonenumber': get_data('phonenumber'),
            'email': get_data('email'),
            'password': get_data('password'),
        }

        if validated_data.get('email') == 'null':
            del validated_data['email']
        if validated_data.get('phonenumber') == 'null':
            del validated_data['phonenumber']

        validator = validate(params)

        if not validator.get('signal'):
            return Response(
                {'errors': validator.get('errors')},
                status=status.HTTP_400_BAD_REQUEST
            )

        for key in params:
            if value := params[key]:
                validated_data[key] = value

        user = UsersSerializer().create(validated_data=validated_data)

        event = Events.objects.get(description='Create account')
        Eventhistory.objects.create(
            event=event,
            user=user,
        )

        return Response(status=status.HTTP_200_OK)


def validate(params):
    errors = []
    to_checked = [
        'phonenumber',
        'email',
    ]
    messages = {
        'phonenumber': f'{params.get("phonenumber")} is already in use',
        'email': f'{params.get("email")} is already in use'
    }

    for param in params:
        if param not in to_checked:
            continue
        try:
            Users.objects.get(**{param: params[param]})
            errors.append(messages[param])
        except Exception as e:
            print(e)

    return {'signal': not errors, 'errors': errors}
