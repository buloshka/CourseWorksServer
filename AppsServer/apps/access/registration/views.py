from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from ...models import Users
from ...serializers import UsersSerializer


class SignUpAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        validated_data = {}
        params = {
            'name': get_data(request, 'name'),
            'surname': get_data(request, 'surname'),
            'fathername': get_data(request, 'fathername'),
            'phonenumber': get_data(request, 'phonenumber'),
            'email': get_data(request, 'email'),
            'password': get_data(request, 'password'),
            'password_again': get_data(request, 'password_again'),
        }

        validator = validate(params)

        if not validator.get('signal'):
            print(validator.get('signal'))
            return Response({'errors': validator.get('errors')}, status=status.HTTP_400_BAD_REQUEST)

        for key in params:
            if key == 'password_again':
                continue
            if value := params[key]:
                validated_data[key] = value

        UsersSerializer().create(validated_data=validated_data)

        return Response({'errors': None}, status=status.HTTP_200_OK)


def get_data(request, name):
    return request.data.get(name) or request.query_params.get(name)


def validate(params):
    errors = []
    checked = [
        'phonenumber',
        'email',
    ]

    if params.get('password') != params.get('password_again'):
        errors.append('password_again')

    for param in params:
        if param not in checked:
            continue
        try:
            if param == 'password_again':
                continue
            Users.objects.get(**{param: params[param]})
            errors.append(param)
        except Exception as e:
            print(e)

    return {'signal': not errors, 'errors': errors}
