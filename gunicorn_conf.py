import os
import multiprocessing

bind = '0.0.0.0:8000'
loglevel = 'debug'
errorlog = '-'
accesslog = '-'
# the formula is based on the assumption that for a given core, one worker
# will be reading or writing from the socket while the other worker is
# processing a request.
workers = os.environ.get('WORKERS', multiprocessing.cpu_count() * 2 + 1)
preload = True
reload = True
worker_class = os.environ.get('WORKER_CLASS', 'gevent')  # async type worker, so the app can handle a stream of requests in parallel
keepalive = 60
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 30))  # 30 is standard default


access_log_format = '{Client-IP: %({X-Real-IP}i)s, Request-time: %(L)s, Request-date: %(t)s, HTTP-Status: "%(r)s", HTTP-Status-Code: %(s)s, Response-length: %(b)s, Http-Referrer: %(f)s, User-Agent: %(a)s}'
