#coding=utf-8
from django import forms

from social_publisher.models import SocialNetwork
from social_publisher.settings import SITE_OWNER


#TODO: create alternative way for handle: (user_networks,site_networks, and publish_on_site_networks)
class PublicationForm(forms.ModelForm):
    user_networks = forms.ModelMultipleChoiceField(queryset=SocialNetwork.objects.none(),
                                                   widget=forms.CheckboxSelectMultiple,
                                                   required=False)
    site_networks = forms.ModelMultipleChoiceField(queryset=SocialNetwork.objects.none(),
                                                   widget=forms.CheckboxSelectMultiple,
                                                   required=False)
    publish_on_site_networks = forms.BooleanField(required=False, initial=False)

    def __init__(self, current_user, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        self.user_networks = None
        self.site_networks = None
        self.user = current_user
        self.fields['user_networks'].queryset = SocialNetwork.objects.filter(enabled=True,
                                                                             social_app__socialtoken__account__user=self.user)
        self.fields['site_networks'].queryset = SocialNetwork.objects.filter(enabled=True,
                                                                             social_app__socialtoken__account__user__id=SITE_OWNER)

    def clean(self):
        self.user_networks = self.cleaned_data['user_networks']
        self.site_networks = self.cleaned_data['site_networks']
        return super(PublicationForm, self).clean()