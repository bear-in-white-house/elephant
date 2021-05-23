from django.utils.module_loading import import_string

from elephant.celery import app
from elephant.settings import MSG_PROVIDER


obj = import_string(MSG_PROVIDER)()


@app.task(bind=True, name='send_mag', queue='others')
def send_msg(self, phone):
    obj.send_msg(phone)


def verify_msg_code(code, phone):
    return obj.verify(code, phone)
