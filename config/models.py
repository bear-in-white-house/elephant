from django.db import models
from django.db.models import JSONField
from rest_framework.utils.encoders import JSONEncoder


class SystemConfigManager(models.Manager):
    def get_data_by_config_key(self, key):
        return self.only('data').get(key=key).data


class SystemConfig(models.Model):
    key = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=50)
    data = JSONField(default=dict, encoder=JSONEncoder)
    objects = SystemConfigManager()

    def __str__(self):
        return self.key
