#coding=utf-8
from django import template
from django.contrib.sites.models import Site
from ..models import SocialNetwork
from ..publisher import VideoProvider, ImageProvider, MessageProvider, ActionMessageProvider
from ..provider import LABEL_TYPE_IMAGE, LABEL_TYPE_VIDEO, LABEL_TYPE_MESSAGE, LABEL_TYPE_ACTION_MESSAGE

register = template.Library()

CONTENT_CLASS = {
    LABEL_TYPE_VIDEO: VideoProvider,
    LABEL_TYPE_IMAGE: ImageProvider,
    LABEL_TYPE_MESSAGE: MessageProvider,
    LABEL_TYPE_ACTION_MESSAGE: ActionMessageProvider
}


@register.assignment_tag(takes_context=True)
def get_social_networks_by_content(context, content):
    if not content in CONTENT_CLASS:
        return None

    publishers = context.get('socialpublisher', {'channels': []})
    channels = publishers.get('channels')
    results = []

    for channel in channels:
        if issubclass(channel, CONTENT_CLASS[content]):
            try:
                results.append(SocialNetwork.objects.get(provider=channel.id, enabled=True))
            except SocialNetwork.DoesNotExist:
                pass

    return results


@register.assignment_tag
def get_current_social_app(social_network):
    return social_network.social_apps.get(
        sites__id=Site.objects.get_current().id
    )