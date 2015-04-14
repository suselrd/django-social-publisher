#coding=utf-8
from django.views.generic.edit import FormView
from forms import PublicationForm


class SocialPublication(FormView):
    form_class = PublicationForm

    def get_form_kwargs(self):
        kwargs = super(SocialPublication, self).get_form_kwargs()
        kwargs.update({
            'current_user': self.request.user
        })
        return kwargs