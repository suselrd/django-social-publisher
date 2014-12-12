#coding=utf-8
from StringIO import StringIO
import logging

from allauth.socialaccount.models import SocialToken, SocialApp
from twython.api import Twython

from social_publisher.provider import ImageProvider, MessageProvider, registry

logger = logging.getLogger(__name__)


class TwitterAdapter(MessageProvider, ImageProvider):
    id = 'twitter'
    name = 'TwitterAdapter'

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.social_token = SocialToken.objects.filter(app__provider='twitter',
                                                       account__provider='twitter',
                                                       account__user=user)
        self.social_app = SocialApp.objects.filter(id=self.social_token.get().app.id)
        self.twitter = Twython(self.social_app.get().client_id, self.social_app.get().secret,
                               self.social_token.get().token,
                               self.social_token.get().token_secret)
        self.twitter.verify_credentials()

    def publish_image(self, image, message='', **kwargs):
        img = open(image.path).read()
        try:
            logger.info('try to update twitter status with an image, for user: %s ' % self.user)
            result = self.twitter.update_status_with_media(status=message, media=StringIO(img))
            logger.debug(str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e

    def publish_message(self, message, **kwargs):
        """
            Attachment:
            {"name": "Link name"
             "link": "http://www.example.com/",
             "caption": "{*actor*} posted a new review",
             "description": "This is a longer description of the attachment",
             "picture": picture}
        """
        try:
            logger.info('try to update twitter status, for user: %s ' % self.user)
            attachment = kwargs.pop('attachment', {})
            message = message or attachment.get('caption', attachment.get('description', ''))
            full_message = "%s (%s)" % (message, attachment.get('link')) if 'link' in attachment else message
            if 'picture' in attachment:
                img = open(attachment.get('picture').path).read()
                result = self.twitter.update_status_with_media(status=full_message, media=StringIO(img))
            else:
                result = self.twitter.update_status(status=full_message)
            logger.debug(str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e


registry.register(TwitterAdapter)