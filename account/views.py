import logging

from rest_framework import mixins, viewsets, views
from rest_framework.response import Response

from account.models import Account
from account.tasks import verify_msg_code
from elephant.permissions import IsMember
from elephant.utils import APIRenderer
from account.tasks import send_msg
from account.serializers import AccountRegisterSerializer
from elephant import constants
from elephant.throttings import ElephantThrottling, GetMsgCodeThrottling


logger = logging.getLogger(__name__)


class AccountLoginViewSet(viewsets.GenericViewSet,
                          mixins.CreateModelMixin):
    model = Account
    queryset = Account.objects.all()
    renderer_classes = [APIRenderer]
    # throttle_classes = [ElephantThrottling]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        try:
            user = Account.objects.select_related('user').get(phone=phone)
        except Account.DoesNotExist:
            return Response(constants.INVALID_USERNAME_OR_PASSWORD, status=400)
        login_type = request.data.get('login_type')
        if login_type == 'password':  # password login
            password = request.data.get('password')
            if not user.user.check_password(password):
                return Response(constants.INVALID_USERNAME_OR_PASSWORD, status=400)
        elif login_type == 'code':  # ver
            code = request.data.get('code')
            if not verify_msg_code(code, user.phone):
                return Response(constants.VERIFICATION_CODE_INVALID, status=400)
        else:
            return Response(constants.INVALID_USERNAME_OR_PASSWORD, status=400)
        request.session['user_id'] = user.id
        return Response(AccountRegisterSerializer(instance=user).data)


class AccountRegisterViewSet(viewsets.GenericViewSet,
                             mixins.CreateModelMixin):
    model = Account
    serializer_class = AccountRegisterSerializer
    renderer_classes = [APIRenderer]
    queryset = Account.objects.all()
    throttle_classes = [ElephantThrottling]
    authentication_classes = []


class GetMsgCode(views.APIView):
    renderer_classes = [APIRenderer]
    throttle_classes = [GetMsgCodeThrottling]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        phone = request.GET.get('phone')
        if not phone:
            return Response(constants.PHONE_REQUIRED, status=400)
        send_msg.delay(phone)
        return Response('ok')


class ResetPassword(views.APIView):
    renderer_classes = [APIRenderer]
    permission_classes = [IsMember]


class AccountInfoViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin):
    model = Account
    queryset = Account.objects.all()
    serializer_class = AccountRegisterSerializer
    renderer_classes = [APIRenderer]
    permission_classes = [IsMember]

    def list(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
