#coding=utf-8
import json
import logging
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from social_publisher.exception import PublisherException
from social_publisher.models import Publication
from social_publisher.provider import VideoProvider, ImageProvider, MessageProvider, registry
from social_publisher.settings import SITE_OWNER


logger = logging.getLogger(__name__)


class Publisher(object):
    def __init__(self, user=None, publish_in_owner_account=None, *args, **kwargs):
        super(Publisher, self).__init__()
        self.user = user
        self.publish_in_owner_account = publish_in_owner_account or False

    def publish_video(self, **kwargs):
        self._validate_kwargs(('video', 'title', 'description', 'networks', 'site_networks'), **kwargs)
        self._publish('publish_video', self.user, self.get_providers(VideoProvider, kwargs.pop('networks')), **kwargs)
        if self.publish_in_owner_account:
            self._publish('publish_video', self.user, self.get_providers(VideoProvider, kwargs.pop('site_networks')),
                          **kwargs)

    def publish_image(self, **kwargs):
        self._validate_kwargs(('image', 'message', 'networks', 'site_networks'), **kwargs)
        self._publish('publish_image', self.user, self.get_providers(ImageProvider, kwargs.pop('networks')), **kwargs)
        if self.publish_in_owner_account:
            self._publish('publish_image', self.get_owner(),
                          self.get_providers(ImageProvider, kwargs.pop('site_networks')), **kwargs)

    def publish_message(self, **kwargs):
        self._validate_kwargs(('message', 'networks', 'site_networks'), **kwargs)
        self._publish('publish_message', self.user, self.get_providers(MessageProvider, kwargs.pop('networks')),
                      **kwargs)
        if self.publish_in_owner_account:
            self._publish('publish_message', self.get_owner(),
                          self.get_providers(MessageProvider, kwargs.pop('site_networks')),
                          **kwargs)

    def _publish(self, fn_name, user, providers, **kwargs):
        publication_args = {'user': user}
        for provider in providers:
            try:
                provider_instance = provider(user)
                if hasattr(provider_instance, fn_name):
                    result = getattr(provider_instance, fn_name)(**kwargs)
                else:
                    return
                publication_args.update({'data': result})
            except Exception as e:
                publication_args.update({'data': json.dumps(str(e))})
            finally:
                #todo if an user have more than one account on same user and same provider :X
                account = SocialAccount.objects.filter(user=user, provider=provider.id).first()
                publication_args.update({'social_account': account})
                if 'instance' in kwargs:
                    instance = kwargs.get('instance')
                    ctype = ContentType.objects.get_for_model(instance)
                    Publication.objects.create(content_type=ctype, object_id=instance.id, **publication_args)

    def get_providers(self, clazz, networks):
        return [p for p in clazz.providers if networks.filter(provider=p.id).exists()]

    def _validate_kwargs(self, to_validate, **kwargs):
        try:
            for arg in to_validate:
                value = kwargs.get(arg, None)
                if value is None:
                    raise AssertionError("the value %s can't be None " % arg)
        except Exception as e:
            raise PublisherException(e)

    def get_owner(self):
        return User.objects.get(id=SITE_OWNER)


def get_publisher(user, publish_in_owner_account):
    registry.load()
    return Publisher(user, publish_in_owner_account)