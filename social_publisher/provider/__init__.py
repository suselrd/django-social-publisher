#coding=utf-8
from django.conf import settings
from django.utils import importlib


class Provider(type):
    def __init__(cls, what, bases=None, args=None):
        if not hasattr(cls, 'providers'):
            cls.providers = []
        else:
            cls.providers.append(cls)
        for clazz in bases:
            if hasattr(clazz, 'providers') and not cls in clazz.providers:
                clazz.providers.append(cls)
        super(Provider, cls).__init__(what, bases, args)


class ImageProvider(object):
    __metaclass__ = Provider

    def publish(self, **kwargs):
        if 'image' in kwargs:
            #TODO:
            return self.publish_image(kwargs.pop('image'), **kwargs)

    def publish_image(self, image, **kwargs):
        """
        """


class VideoProvider(object):
    __metaclass__ = Provider

    def publish(self, **kwargs):
        if 'video' in kwargs:
            #TODO:
            return self.publish_video(kwargs.pop('video'), **kwargs)

    def publish_video(self, video, **kwargs):
        """
        """


class MessageProvider(object):
    __metaclass__ = Provider

    def publish(self, **kwargs):
        if 'message' in kwargs:
            #TODO:
            return self.publish_message(kwargs.pop('message'), **kwargs)

    def publish_message(self, message, **kwargs):
        """
        """


class Registry(object):
    """
    copy from allauth
    """

    def __init__(self):
        self.adapter_map = {}
        self.loaded = False

    def get_list(self):
        self.load()
        return self.adapter_map.values()

    def register(self, cls):
        self.adapter_map[cls.id] = cls

    def by_id(self, id):
        self.load()
        return self.adapter_map[id]

    def as_choices(self):
        for adapter in self.get_list():
            yield (adapter.id, adapter.name)

    def load(self):
        if not self.loaded:
            for adapter in settings.PUBLISHERS or ():
                adapter_module = adapter + '.' + 'adapter'
                try:
                    importlib.import_module(adapter_module)
                except ImportError as e:
                    pass
            self.loaded = True


registry = Registry()