#coding=utf-8
from StringIO import StringIO
import logging

from allauth.socialaccount.models import SocialToken, SocialApp
from twython.api import Twython

from social_publisher.provider import ImageProvider, MessageProvider, ActionMessageProvider, registry

logger = logging.getLogger(__name__)


class TwitterAdapter(MessageProvider, ImageProvider, ActionMessageProvider):
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
        try:
            logger.info('try to update twitter status, for user: %s ' % self.user)
            result = self.twitter.update_status(status=message)
            logger.debug(str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e

    def publish_action_message(self, message, action_info, **kwargs):
        """
            action_info: dictionary with information about the corresponding app activity/action
            {
                 "link": the url for the app activity/action to point to,
                 "actor": the actor,
                 "action": the action performed by 'actor',
                 "verb": the verbal form to show for the action performed by 'actor',
                 "target": the target of the action,
                 "app": the application name,
                 "domain": the application domain
                 "picture": the picture to show
             }
        """
        try:
            logger.info('try to update twitter status, for user: %s ' % self.user)
            from django.utils.translation import ugettext as _

            message = message or "%s (%s) %s %s" % (
                action_info.get('action', ''),
                action_info.get('target', ''),
                _(u'using'),
                action_info.get('app', _(u'application'))
            ),
            full_message = "%s (%s)" % (message, action_info.get('link')) if 'link' in action_info else message
            if 'picture' in action_info:
                img = open(action_info.get('picture').path).read()
                result = self.twitter.update_status_with_media(status=full_message, media=StringIO(img))
            else:
                result = self.twitter.update_status(status=full_message)
            logger.debug(str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e

registry.register(TwitterAdapter)