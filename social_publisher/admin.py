#coding=utf-8
from django.contrib.admin import site
from social_publisher.models import SocialNetwork, SocialNetworkApp, Publication

site.register((SocialNetwork, SocialNetworkApp, Publication))