import os
import base64
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from PIL import Image, ImageDraw

from django.db.models import Sum, Max
from django.utils import timezone


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from ...models import Users, Purchasehistory, Eventhistory, Subscriptions, Events
from ...serializers import (SubscriptionsSerializer,
                            UsersSerializer,)

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


def get_entry_frequency(user: Users) -> float:
    # Хранение разницы между датами
    frequency_list: list[int] = []
    event: Eventhistory.objects = Events.objects.get(description='Sign in')
    # Получение всех записей вхождения пользователем в приложение
    entries: Eventhistory.objects = Eventhistory.objects.filter(
        user=user,
        event=event,
    )
    for i in range(len(entries) - 1):
        # Находим интервал между датами
        interval: timedelta = entries[i+1].event_date - entries[i].event_date
        frequency_list.append(interval.days)
    len_dates: int = len(frequency_list) if len(frequency_list) else 1
    return sum(frequency_list) / len_dates


def get_total_sum(user: Users) -> int | float:
    # Находим историю покупок пользователя и складываем все цены
    total_sum: int | float = Purchasehistory.objects.filter(
        user=user
    ).aggregate(Sum('sub__price'))['sub__price__sum'] or 0

    return float(total_sum)


def get_stay_months(user: Users) -> int:
    # Находим разницу между датами
    time_difference: timedelta | datetime = timezone.now() - user.registration_date
    # Вычисляем кол-во месяцев
    stay_months: int = int(time_difference.total_seconds() / (30.44 * 24 * 60 * 60))

    return stay_months


def get_months_from_last_purchase(user: Users) -> int:
    # Находим дату последней покупки пользователя
    last_purchase: datetime = Purchasehistory.objects.filter(
        user=user
    ).aggregate(Max('purchase_date'))['purchase_date__max']

    if not last_purchase:
        return 0

    year: int = last_purchase.year
    month: int = last_purchase.month
    # Находим кол-во месяцев между датами
    stay_months: int = (
        (timezone.now().year - year) * 12 +
        timezone.now().month - month
    )

    return stay_months


def get_purchases_frequency(user: Users) -> float:
    # Хранение разницы между датами
    frequency_list: list[int] = []
    # Находим историю покупки пользователя
    purchases: Purchasehistory.objects = Purchasehistory.objects.filter(
        user=user,
    )
    for i in range(len(purchases) - 1):
        # Находим интервал между датами
        interval: timedelta = purchases[i + 1].purchase_date - purchases[i].purchase_date
        frequency_list.append(interval.days)
    len_dates: int = len(frequency_list) if len(frequency_list) else 1
    return sum(frequency_list) / len_dates


def get_users() -> list[dict[str, int | float]]:
    random_users: list[Users] = list(Users.objects.all().order_by('?'))
    users: list[dict[str, int | float]] = []
    for user in random_users:
        users.append({
            'id': user.id,
            'entry_count': get_entry_frequency(user),
            'total_sum': get_total_sum(user),
            'stay_months': get_stay_months(user),
            'months_from_last_purchase': get_months_from_last_purchase(user),
            'purchase_count_last_year': get_purchases_frequency(user),
        })
    return users


def normalize_values(users_data: list[dict[str, int | float]],
                     weights: tuple[float, float, float, float, float] = None) \
        -> list[dict[str, int | float]]:
    if not weights:
        weights = (0.7, 0.8, 0.65, -0.4, 0.8)
    normalized_data: list[dict[str, int | float]] = users_data.copy()

    normalized_values: list[list[int | float]] = [
        [user['entry_count'], user['total_sum'], user['stay_months'], user['months_from_last_purchase'], user['purchase_count_last_year']]
        for user in normalized_data
    ]

    for i in range(len(normalized_values[0])):
        max_value = max([sublist[i] for sublist in normalized_values])
        max_value = max_value if max_value else 1
        for j in range(len(normalized_values)):
            normalized_values[j][i] = normalized_values[j][i] / max_value * weights[i]

    for i, user in enumerate(normalized_data):
        user['entry_count']: int = normalized_values[i][0]
        user['total_sum']: int | float = normalized_values[i][1]
        user['stay_months']: int = normalized_values[i][2]
        user['months_from_last_purchase']: int = normalized_values[i][3]
        user['purchase_count_last_year']: int = normalized_values[i][4]

    return normalized_data


def get_additive_criterion(users_data: list[dict[str, int | float]]) -> list[dict[str, int | float]]:
    results: list[dict[str, int | float]] = []
    sums: dict[str, int | float] = {
        'entry_count': 0,
        'total_sum': 0,
        'stay_months': 0,
        'months_from_last_purchase': 0,
        'purchase_count_last_year': 0,
    }
    for user in users_data:
        sums['entry_count'] += user['entry_count']
        sums['total_sum'] += user['total_sum']
        sums['stay_months'] += user['stay_months']
        sums['months_from_last_purchase'] += user['months_from_last_purchase']
        sums['purchase_count_last_year'] += user['purchase_count_last_year']

    addetive: int | float = sum(sums.values())
    addetive = addetive if addetive else 1
    for user in users_data:
        id: int = user.pop('id')
        addetive_criterion: int | float = sum(user.values()) / addetive
        results.append({
            'user_id': id,
            'criterion': addetive_criterion
        })

    return results


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


class GetUserProfileAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)

        user_id = int(get_data('user_id'))
        user = Users.objects.get(id=user_id)

        user_data = UsersSerializer(user).data

        date_string = user_data.get('registration_date')
        try:
            datetime_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f+03:00')
        except ValueError:
            datetime_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S+03:00')
        formatted_date = datetime_object.strftime('%d.%m.%Y %H:%M:%S.%f')
        date, time = formatted_date.split(' ')
        hhmm = time[:time.rfind(':'):]
        user_data['registration_date'] = ' '.join((date, hhmm))

        avatar = user_data.get('avatar')
        point = avatar.rfind('/') + 1
        filename = avatar[point::]
        path = MAIN_DIR + avatar[:point:]

        user_data['avatar'] = round_image(path, filename)

        del user_data['token']

        users = get_users()
        normalized = normalize_values(users)
        additive = get_additive_criterion(normalized)
        user = [user for user in additive if user['user_id'] == user_id].pop()

        subscriptions = Subscriptions.objects.all()
        subs = []
        for sub in subscriptions:
            discount = Decimal(round(user['criterion'], 2))
            sub.price -= sub.price * Decimal(round(user['criterion'], 2))
            sub_data = SubscriptionsSerializer(sub).data
            del sub_data['chats'], sub_data['media']
            del sub_data['analytics'], sub_data['themes']
            descriptions = {
                '- Дополнительные возможности в чатах': sub.chats,
                '- Увеличенное хранилище для медиа файлов': sub.media,
                '- Возможность просматривать аналитику': sub.analytics,
                '- Уникальные темы, которые можно ставить всем участникам чата': sub.themes,
            }
            description = '\n'.join((key for key in descriptions.keys() if descriptions[key]))
            sub_data['description'] = description
            sub_data['discount_percent'] = round(discount * 100)
            subs.append(sub_data)

        if user_data['fathername'] is None:
            user_data['fathername'] = ''

        latest_purchase = Purchasehistory.objects.filter(
            user_id=user_id,
            purchase_date__gte=datetime.now() - relativedelta(months=1)
        ).aggregate(Max('purchase_date'))

        sub = None
        if latest_purchase:
            history = Purchasehistory.objects.filter(
                user_id=user_id,
                purchase_date=latest_purchase['purchase_date__max']
            ).first()
            if history:
                sub = SubscriptionsSerializer(history.sub).data

        return Response(
            {'user': user_data, 'subs': subs, 'active_sub': sub,},
            status=status.HTTP_200_OK)


class BuySubscriptionAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def put(self, request):
        def get_data(name):
            return request.query_params.get(name) or request.data.get(name)
        user_id = int(get_data('user_id'))
        sub_id = int(get_data('sub_id'))
        sub_price = Decimal(float(get_data('sub_price').replace(',', '.')))

        user = Users.objects.get(id=user_id)
        sub = Subscriptions.objects.get(id=sub_id)
        latest_purchase = Purchasehistory.objects.filter(
            user=user,
            sub=sub,
        ).aggregate(Max('purchase_date'))

        history = Purchasehistory.objects.filter(
            user=user,
            sub=sub,
            purchase_date=latest_purchase['purchase_date__max']
        ).first()

        continue_sub = False
        if history and history.purchase_date > timezone.now() - relativedelta(months=1):
            event = Events.objects.get(description='Sub renewal')
            continue_sub = True
        else:
            event = Events.objects.get(description='Buy sub')

        Eventhistory.objects.create(
            event=event,
            user=user,
        )

        if continue_sub:
            Purchasehistory.objects.create(
                user=user,
                sub=sub,
                price=sub_price,
                purchase_date=history.purchase_date + relativedelta(months=1),
            )
        else:
            Purchasehistory.objects.create(
                user=user,
                sub=sub,
                price=sub_price,
            )

        return Response(status=status.HTTP_201_CREATED)
