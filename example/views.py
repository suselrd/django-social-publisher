#coding=utf-8
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import CreateView
from example.forms import ArticleForm
from example.models import Article
from social_publisher.publisher import get_publisher


class CreateArticleView(CreateView):
    template_name = 'example/form.html'
    model = Article
    form_class = ArticleForm

    def get_success_url(self):
        return reverse('create_article')

    def get_form_kwargs(self):
        form_kwargs = super(CreateArticleView, self).get_form_kwargs()
        form_kwargs['current_user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        #save the object or...
        self.object.save()
        #retreive the publisher for the current user
        publisher = get_publisher(self.request.user, form.cleaned_data['publish_on_site_networks'])
        #retreive the selected networks
        networks = form.cleaned_data['user_networks']
        #retreive the selected site networks
        site_networks = form.cleaned_data['site_networks']
        #message
        message = form.cleaned_data['twitter']
        #video
        video = self.object.video
        #image
        image = self.object.image
        result = '' #-->for testing
        try:
            #message ( message, networks, site_networks)
            message += ' ' + self.request.build_absolute_uri(location=reverse('create_article'))
            # if message contains an url (22 for http, 23 for https) characters reserved url in twitter
            result = publisher.publish_message(message=message, networks=networks, site_networks=site_networks,
                                               instance=self.object)
        except Exception as e:
            print('message', e)
        finally:
            print('message', result)
        try:
            #video (video, title, description, networks, site_networks)
            result = publisher.publish_video(video=video, title='titulo del video',
                                             description=form.cleaned_data['summary'],
                                             networks=networks, site_networks=site_networks, instance=self.object)
        except Exception as e:
            print('video', e)
        finally:
            print('video', result)
        try:
            #image (image, message, networks, site_networks)
            # if message contains an url (22 for http, 23 for https) characters reserved url in twitter
            # if message contains a picture 23 character reserved
            result = publisher.publish_image(image=image, message=message, networks=networks,
                                             site_networks=site_networks, instance=self.object)
        except Exception as e:
            print('image', e)
        finally:
            print('image', result)

        return HttpResponseRedirect(self.get_success_url())
    