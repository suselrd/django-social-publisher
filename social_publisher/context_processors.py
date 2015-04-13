#coding=utf-8
from . import provider


def socialpublisher(request):
    ctx = {
        'providers': provider.registry.get_list()
    }
    return dict(socialpublisher=ctx)
