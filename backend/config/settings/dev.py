import socket
from config.settings.common import *  # noqa

SECRET_KEY = "django-insecure-74!21)tgkyark5kh8*p@wv_u76=_5h$13!fpfh=ya$2(nd(mg9"
DEBUG = True

if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
    ALLOWED_HOSTS = ["*"]

SILK_ENABLED = False
SILK_TRACK_MIDDLEWARES = False

if SILK_ENABLED:
    INSTALLED_APPS += ("silk",)
    if SILK_TRACK_MIDDLEWARES:
        MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")
    else:
        MIDDLEWARE.append("silk.middleware.SilkyMiddleware")

    SILKY_AUTHENTICATION = False
    SILKY_AUTHORISATION = False
