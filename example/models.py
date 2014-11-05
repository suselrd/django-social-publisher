#coding=utf-8
from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    creator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    summary = models.CharField(max_length=255)
    twitter = models.CharField(max_length=140)
    image = models.ImageField(upload_to='article/image', max_length=255)
    video = models.FileField(upload_to='article/video', max_length=255)
