#coding=utf-8
import json
import logging
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from allauth.socialaccount.models import SocialAccount
from social_publisher.exception import PublisherException
from social_publisher.models import Publication, SocialNetwork
from social_publisher.provider import VideoProvider, ImageProvider, MessageProvider, ActionMessageProvider, registry
from social_publisher.settings import SITE_OWNER


logger = logging.getLogger(__name__)


class Publisher(object):
    def __init__(self, user=None, publish_in_owner_account=None, *args, **kwargs):
        super(Publisher, self).__init__()
        self.user = user
        self.publish_in_owner_account = publish_in_owner_account or False

    def publish_video(self, **kwargs):
        self._validate_kwargs(('video', 'title', 'description', 'networks'), **kwargs)
        self._publish('publish_video', self.user, self.get_providers(VideoProvider, kwargs.pop('networks')), **kwargs)
        if self.publish_in_owner_account and kwargs.get('site_networks', None) is not None:
            self._publish('publish_video', self.user, self.get_providers(VideoProvider, kwargs.pop('site_networks')),
                          **kwargs)

    def publish_image(self, **kwargs):
        self._validate_kwargs(('image', 'message', 'networks'), **kwargs)
        self._publish('publish_image', self.user, self.get_providers(ImageProvider, kwargs.pop('networks')), **kwargs)
        if self.publish_in_owner_account and kwargs.get('site_networks', None) is not None:
            self._publish('publish_image', self.get_owner(),
                          self.get_providers(ImageProvider, kwargs.pop('site_networks')), **kwargs)

    def publish_message(self, **kwargs):
        self._validate_kwargs(('message', 'networks'), **kwargs)
        self._publish('publish_message', self.user, self.get_providers(MessageProvider, kwargs.pop('networks')),
                      **kwargs)
        if self.publish_in_owner_account and kwargs.get('site_networks', None) is not None:
            self._publish('publish_message', self.get_owner(),
                          self.get_providers(MessageProvider, kwargs.pop('site_networks')),
                          **kwargs)

    def publish_action_message(self, **kwargs):
        self._validate_kwargs(('message', 'action_info', 'networks'), **kwargs)
        self._publish('publish_action_message', self.user, self.get_providers(ActionMessageProvider, kwargs.pop('networks')),
                      **kwargs)
        if self.publish_in_owner_account and kwargs.get('site_networks', None) is not None:
            self._publish('publish_action_message', self.get_owner(),
                          self.get_providers(ActionMessageProvider, kwargs.pop('site_networks')),
                          **kwargs)

    def _publish(self, fn_name, user, providers, **kwargs):
        publication_args = {'user': user}
        for provider in providers:
            try:
                provider_instance = provider(user)
                if hasattr(provider_instance, fn_name):
                    result = getattr(provider_instance, fn_name)(**kwargs)
                else:
                    continue
                publication_args.update({'data': result})
            except Exception as e:
                publication_args.update({'data': json.dumps(str(e))})
            finally:
                #todo if an user have more than one account on same user and same provider :X
                social_network = SocialNetwork.objects.get(provider=provider.id)
                account = SocialAccount.objects.filter(
                    user=user,
                    provider__in=[network_app.social_app.provider for network_app in social_network.social_apps.all()]
                ).first()
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