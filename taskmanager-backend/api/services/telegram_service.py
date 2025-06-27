from ..serializers import TelegramLoginSerializer
from ..models import TelegramUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class TelegramService:
    def __init__(self):
        self.TelegramUser = TelegramUser.objects

    def login_telegram(self, data):
        try:
            serializer = TelegramLoginSerializer(data=data)
            if not serializer.is_valid():
                return {'success': False, 'message': serializer.errors}

            telegram_id = serializer.validated_data['telegram_id']

            try:
                profile = self.TelegramUser.select_related('user').get(telegram_id=telegram_id)
                user = profile.user
            except TelegramUser.DoesNotExist:
                username = f"tg_{telegram_id}"
                user = User.objects.create_user(username=username)
                TelegramUser.objects.create(user=user, telegram_id=telegram_id)

            token, created = Token.objects.get_or_create(user=user)

            return {
                'success': True,
                'message': 'Авторизация успешна',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'token': token.key,
                }
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}