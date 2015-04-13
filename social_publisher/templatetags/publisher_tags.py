#coding=utf-8
from django import template
from ..models import SocialNetwork
from ..publisher import VideoProvider, ImageProvider, MessageProvider, ActionMessageProvider

register = template.Library()

CONTENT_CLASS = {
    'video': VideoProvider,
    'image': ImageProvider,
    'message': MessageProvider,
    'action_message': ActionMessageProvider
}

@register.assignment_tag(takes_context=True)
def get_social_networks_by_content(context, content):
    if not content in CONTENT_CLASS:
        return None

    publishers = context.get('socialpublisher', {'channels': []})
    channels = publishers.get('channels')
    results = []

    for channel in channels:
        if isinstance(channel, CONTENT_CLASS[content]):
            try:
                results.append(SocialNetwork.objects.get(provider=channel.id, enabled=True))
            except SocialNetwork.DoesNotExist:
                pass

    return results