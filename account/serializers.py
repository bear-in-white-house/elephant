from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction

from account.models import Account
from elephant import constants
from account.tasks import verify_msg_code
from elephant.utils.utils import is_valid_password


class AccountSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('is_admin', 'avatar', 'username')

    def validate(self, attrs):
        username = attrs.get('username')
        phone = self.context['request'].user.phone
        code = attrs.pop('code', None)
        if not code or not verify_msg_code(code, phone):
            raise serializers.ValidationError(constants.VERIFICATION_CODE_INVALID)
        if username is not None and 6 <= len(username) <= 20:
            raise serializers.ValidationError(constants.INVALID_USERNAME)
        password = attrs.get('password')
        if password is not None and not is_valid_password(password):
            raise serializers.ValidationError(constants.INVALID_PASSWORD)
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.use.set_password(password)
        return instance


class AccountRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20, write_only=True)
    username = serializers.CharField(read_only=True)
    avatar = serializers.FileField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Account
        fields = ('user_id', 'phone', 'username', 'avatar', 'is_admin')

    def validate(self, attrs):
        phone = attrs.get('phone')
        if not phone:
            raise serializers.ValidationError(constants.PHONE_REQUIRED)

        code = attrs.pop('code', None)
        if not code or not verify_msg_code(code, phone):
            raise serializers.ValidationError(constants.VERIFICATION_CODE_INVALID)

        password = attrs.get('password')
        if not password or not is_valid_password(password):
            raise serializers.ValidationError(constants.INVALID_PASSWORD)

        if Account.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(constants.PHONE_ALREADY_EXISTS)

        return attrs

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['code'] = data.get('code')
        ret['password'] = data.get('password')
        return ret

    def create(self, validated_data):
        password = validated_data.pop('password')

        with transaction.atomic():
            validated_data['username'] = f'贴吧用户_{validated_data["phone"]}'
            user = User.objects.create(username=validated_data['username'])
            user.set_password(password)
            validated_data['user'] = user
            instance = super().create(validated_data)
        return instance
