#coding=utf-8
from django.contrib.admin import site
from social_publisher.models import SocialNetwork, Publication

site.register((SocialNetwork, Publication))