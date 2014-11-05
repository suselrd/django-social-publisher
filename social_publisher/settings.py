#coding=utf-8
from django.conf import settings

PUBLISHERS = getattr(settings, 'PUBLISHERS', ())
SITE_OWNER = getattr(settings, 'SITE_OWNER', 1)