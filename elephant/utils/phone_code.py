import hmac
import json
import random
import logging
import hashlib
import base64
from uuid import uuid4
from abc import ABC, abstractmethod
from urllib.parse import quote, urlencode

import requests
from django.core.cache import cache
from django.utils.timezone import now

from config.models import SystemConfig
from elephant.utils.exceptions import SendMsgError

logger = logging.getLogger(__name__)


class BasePhoneCode(ABC):
    @abstractmethod
    def send_msg(self, phone):
        """
        code: 验证码,
        phone: 手机号
        """

    @abstractmethod
    def verify(self, code, phone):
        """
        code: 验证码,
        phone: 手机号
        return: bool
        """


class AliMsgCode(BasePhoneCode):
    NAME = '阿里云发送短信'
    TIME_OUT = 60 * 500000
    CONFIG_KEY = 'AliMsgCode'
    HOST = 'http://dysmsapi.aliyuncs.com/'

    @staticmethod
    def generate_code():
        return str(random.randint(1000, 9999))

    def send_msg(self, phone):
        code = self.generate_code()
        data = self.generate_data(code, phone)
        uri = self.make_uri(self.HOST, data)
        try:
            res = requests.get(uri).json()
            ret_code = res['Code']
            if not ret_code == 'OK':
                raise Exception(f'code is : {ret_code}')
        except Exception as e:
            logger.exception(e)
            raise SendMsgError(f'send msg failed : detais: {e}')
        else:
            cache.set(f'{self.CONFIG_KEY}{phone}', code, timeout=self.TIME_OUT)

    @classmethod
    def verify(cls, code, phone):
        cache_code = cache.get(f'{cls.CONFIG_KEY}{phone}')
        return bool(cache_code and code == cache_code)

    @staticmethod
    def make_uri(host, data):
        url_data = urlencode(data)
        return f'{host}?{url_data}'

    @staticmethod
    def sign(data, token):
        sign_str = '&'.join([f'{key}={value}' for key, value in sorted(data.items())])
        hmac_s2 = 'GET&%2F&' + quote(quote(sign_str, safe='=&'))
        hmac_s1 = token + '&'
        res_s = hmac.new(hmac_s1.encode(), hmac_s2.encode(), hashlib.sha1).digest()
        return base64.b64encode(res_s).decode()

    def generate_data(self, code, phone):
        data = SystemConfig.objects.get_data_by_config_key(self.CONFIG_KEY)
        params = {
            'AccessKeyId': data['AccessKey'],
            'Timestamp': now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'Format': 'json',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureVersion': '1.0',
            'SignatureNonce': uuid4().hex,
            'Action': 'SendSms',
            'Version': '2017-05-25',
            'RegionId': 'cn-hangzhou',
            'PhoneNumbers': phone,
            'SignName': '乐理二手',
            'TemplateCode': 'SMS_163438002',
            'TemplateParam': json.dumps({'code': code})
        }
        params['Signature'] = self.sign(params, data['SecretKey'])
        return params
