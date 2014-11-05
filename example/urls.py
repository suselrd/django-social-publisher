#coding=utf-8
from django.conf.urls import patterns, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from example.views import CreateArticleView

admin.autodiscover()

urlpatterns = \
    patterns('',
             url(r'^$', login_required(CreateArticleView.as_view()), name='create_article'),

    )