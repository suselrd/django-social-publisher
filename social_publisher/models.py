#coding=utf-8
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from allauth.socialaccount.fields import JSONField
from allauth.socialaccount.models import SocialAccount, SocialApp
from provider import registry


@python_2_unicode_compatible
class SocialNetwork(models.Model):
    """
     Represents a social network, to publish to.
    """
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    provider = models.CharField(max_length=50, choices=registry.as_choices(), unique=True)
    social_apps = models.ManyToManyField(SocialApp, related_name='social_networks')

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Publication(models.Model):
    """
    Store all publications
    """
    user = models.ForeignKey(User)
    social_account = models.ForeignKey(SocialAccount)
    data = JSONField(default='{}')
    create_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "Publication: %d " % self.id