import os
import re
from uuid import uuid4

from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]

        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)

        # return the whole path to the file
        return os.path.join(self.path, filename)


def is_valid_password(password):
    re_str = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
    return bool(re.match(re_str, password))
