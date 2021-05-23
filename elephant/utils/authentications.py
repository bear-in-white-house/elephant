from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from account.models import Account
from elephant import constants


class ElephantAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return None, None
        try:
            user = Account.objects.select_related('user').get(id=user_id)
            if not user.user.is_active:
                request.session.flush()
                raise AuthenticationFailed(constants.INVALID_ACCOUNT)
        except Account.DoesNotExist:
            user = None
        return user, None
