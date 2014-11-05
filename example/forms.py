#coding=utf-8
from django.forms.widgets import Textarea
from example.models import Article
from social_publisher.forms import PublicationForm


class ArticleForm(PublicationForm):
    class Meta:
        model = Article
        fields = ('text', 'summary', 'twitter', 'image', 'video')
        widgets = {
            'summary': Textarea,
            'twitter': Textarea,
        }