from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from sms import send_sms
from twilio.rest import Client

from ...models import Users
from ...serializers import UsersSerializer


class ValidateUserAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        def get_data(name):
            return request.data.get(name) or request.query_params.get(name)

        data = {}
        if email := get_data('email'):
            data['email'] = email
        if phonenumber := get_data('phonenumber'):
            data['phonenumber'] = phonenumber
            data['type'] = get_data('type') or '0'

        validator = validate(data)

        if validator.get('signal'):
            return Response({'errors': validator.get('errors')}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': None}, status=status.HTTP_200_OK)


class ValidateCodeAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        def get_data(name):
            return request.data.get(name) or request.query_params.get(name)
        data = {'code': get_data('code')}

        validator = validate(data)

        if validator.get('signal'):
            return Response({'errors': validator.get('errors')}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': None}, status=status.HTTP_200_OK)


class RefreshPasswordAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        def get_data(name):
            return request.data.get(name) or request.query_params.get(name)
        data = {
            'code': get_data('code'),
            'new_password': get_data('new_password'),
        }

        try:
            user = Users.objects.get(code=data['code'])
        except Exception as e:
            return Response({'errors': "code doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        suser = UsersSerializer(user)

        signal = suser.set_password(user, data['new_password'])
        if not signal:
            return Response({'errors': 'expired_code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': None}, status=status.HTTP_200_OK)


def send_email(user, to):
    subject = "Recovery code"
    from_email = settings.EMAIL_HOST_USER

    serialized_user = UsersSerializer(user)
    userdata = serialized_user.data
    fullname = ' '.join([
        userdata.get('name'),
        userdata.get('surname'),
        userdata.get('fathername'),
    ])

    context = {
        'fullname': fullname,
        'code': serialized_user.generate_code(user),
    }
    html_content = render_to_string('./email.html', context)

    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        [to]
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_message(user, to):
    serialized_user = UsersSerializer(user)
    userdata = serialized_user.data
    fullname = ' '.join([
        userdata.get('name').title(),
        userdata.get('surname').title(),
        userdata.get('fathername').title(),
    ])

    if not to.startswith('+'):
        to = ''.join(('+', str(int(to[0]) - 1), to[1:]))

    text = f'\n\n{fullname}, your recovery code is '\
           + serialized_user.generate_code(user)\
           + '\nDon\'t share the code with anyone.'

    send_sms(
        text,
        settings.TWILIO_PHONE_NUMBER,
        [to],
        fail_silently=False
    )


def send_voice_message(user, to):
    serialized_user = UsersSerializer(user)
    userdata = serialized_user.data
    fullname = ' '.join([
        userdata.get('name').title(),
        userdata.get('surname').title(),
        userdata.get('fathername').title(),
    ])

    if not to.startswith('+'):
        to = ''.join(('+', str(int(to[0]) - 1), to[1:]))

    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
    )

    text = 'Ваш код... ' + '... '.join(serialized_user.generate_code(user))
    text = text + ("... Повторяю... " + text) * 2
    message = client.calls.create(
        twiml=f'<Response><Say language="ru-RU" voice="woman">{text}</Say></Response>',
        to=to,
        from_=settings.TWILIO_PHONE_NUMBER,
    )


def validate(params):
    errors = ''
    to_checked = [
        'phonenumber',
        'email',
        'code',
    ]
    messages = {
        'phonenumber': 'Phone number is invalid pr doesn\'t exist',
        'email': 'Email is invalid or doesn\'t exist',
        'code': 'Code is invalid',
    }

    for param in params:
        if param not in to_checked:
            continue
        try:
            user = Users.objects.get(**{param: params[param]})
            if param == 'email':
                send_email(user, params[param])
            if param == 'phonenumber':
                type = params['type']
                if type == '0':
                    send_message(user, params[param])
                else:
                    send_voice_message(user, params[param])
            if param == 'code' and UsersSerializer(user).is_code_expired(user):
                errors += messages[param]
        except Exception as e:
            errors += messages[param]

    return {'signal': errors, 'errors': errors}
