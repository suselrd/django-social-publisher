# coding=utf-8
from django.dispatch import Signal

publication_in_channel = Signal(
    providing_args=["instance", "channel_type", "channel", "user", "social_account", "status", "data"]
)
publication = Signal(providing_args=["instance", "channel_type", "user", "results"])
