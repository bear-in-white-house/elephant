from rest_framework.throttling import AnonRateThrottle

from config.models import SystemConfig


class ElephantThrottling(AnonRateThrottle):
    def get_cache_key(self, request, view):
        scope = f'{self.scope}{view.__class__}'
        return self.cache_format % {
            'scope': scope,
            'ident': self.get_ident(request)
        }

    def get_rate(self):
        data = SystemConfig.objects.get_data_by_config_key('default_throttling')
        return data['rate']


class GetMsgCodeThrottling(ElephantThrottling):
    def get_rate(self):
        return '1/m'
