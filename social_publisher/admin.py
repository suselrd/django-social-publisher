#coding=utf-8
from django.contrib import admin
from social_publisher.models import SocialNetwork, Publication


admin.site.register(SocialNetwork)
admin.site.register(Publication)