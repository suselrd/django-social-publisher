#coding=utf-8
from django.views.generic.edit import FormView
from social_publisher.forms import PublicationForm


class SocialPublication(FormView):
    def get_context_data(self, **kwargs):
        context_data = super(SocialPublication, self).get_context_data(**kwargs)
        context_data['social_publication_form'] = PublicationForm(self.request.user)
        return context_data