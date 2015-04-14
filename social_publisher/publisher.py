#coding=utf-8
import json
import logging
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from exception import PublisherException
from models import SocialNetwork
from provider import VideoProvider, ImageProvider, MessageProvider, ActionMessageProvider, registry
from settings import SITE_OWNER
from signals import publication_in_channel, publication


logger = logging.getLogger(__name__)


class Publisher(object):
    def __init__(self, user=None, publish_in_owner_account=False, *args, **kwargs):
        super(Publisher, self).__init__()
        self.user = user
        self.publish_in_owner_account = publish_in_owner_account
        if self.publish_in_owner_account and not self.user:
            self.user = self._get_owner()

    def publish_video(self, **kwargs):
        self._validate_kwargs(('video', 'title', 'description', 'networks'), **kwargs)
        self._publish(
            'publish_video',
            VideoProvider,
            **kwargs
        )

    def publish_image(self, **kwargs):
        self._validate_kwargs(('image', 'message', 'networks'), **kwargs)
        self._publish(
            'publish_image',
            ImageProvider,
            **kwargs
        )

    def publish_message(self, **kwargs):
        self._validate_kwargs(('message', 'networks'), **kwargs)
        self._publish(
            'publish_message',
            MessageProvider,
            **kwargs
        )

    def publish_action_message(self, **kwargs):
        self._validate_kwargs(('message', 'action_info', 'networks'), **kwargs)
        self._publish(
            'publish_action_message',
            ActionMessageProvider,
            **kwargs
        )

    def _publish(self, fn_name, channel_type, **kwargs):
        if not self.user:
            return None
        providers = self._get_providers(channel_type, kwargs.pop('networks'))
        instance = kwargs.get('instance', None)
        results = {}
        for provider in providers:
            try:
                provider_instance = provider(self.user)
                if hasattr(provider_instance, fn_name):
                    data = getattr(provider_instance, fn_name)(**kwargs)
                    status = "SUCCESS"
                else:
                    continue
            except Exception as e:
                data = json.dumps(str(e))
                status = "ERROR"
            finally:
                #todo if an user have more than one account on same user and same provider :X
                account = SocialAccount.objects.filter(
                    user=self.user,
                    provider__in=[
                        social_app.provider
                        for social_app in SocialNetwork.objects.get(provider=provider.id).social_apps.all()
                    ]
                ).first()
                results.update({
                    provider.id: {
                        "status": status,
                        "response": data,
                        'social_account': account
                    }
                })
                publication_in_channel.send(
                    sender=type(instance),
                    instance=instance,
                    user=self.user,
                    channel_type=channel_type,
                    channel=provider.id,
                    social_account=account,
                    data=data,
                    status=status
                )

        publication.send(
            sender=type(instance),
            instance=instance,
            user=self.user,
            channel_type=channel_type,
            results=results
        )

    def _get_providers(self, clazz, networks):
        return [p for p in clazz.providers if networks.filter(provider=p.id).exists()]

    def _validate_kwargs(self, to_validate, **kwargs):
        try:
            for arg in to_validate:
                value = kwargs.get(arg, None)
                if value is None:
                    raise AssertionError("the value %s can't be None " % arg)
        except Exception as e:
            raise PublisherException(e)

    def _get_owner(self):
        return User.objects.get(id=SITE_OWNER)


def get_publisher(user=None, publish_in_owner_account=False):
    registry.load()
    return Publisher(user, publish_in_owner_account)