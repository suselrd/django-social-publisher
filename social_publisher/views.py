#coding=utf-8
from django.views.generic.edit import FormView
from social_publisher.forms import PublicationForm


class SocialPublication(FormView):
    def get_context_data(self, **kwargs):
        context_data = super(SocialPublication, self).get_context_data(**kwargs)
        context_data['social_publication_form'] = PublicationForm(self.request.user)
        return context_data

    def post(self, request, *args, **kwargs):
        return super(SocialPublication, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(SocialPublication, self).get_form_class()

    def get_form(self, form_class):
        return super(SocialPublication, self).get_form(form_class)

    def get_form_kwargs(self):
        return super(SocialPublication, self).get_form_kwargs()

