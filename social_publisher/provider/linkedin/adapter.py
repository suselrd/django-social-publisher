#coding=utf-8
import logging
from allauth.socialaccount.models import SocialToken, SocialApp
from linkedin import linkedin
from social_publisher.provider import ActionMessageProvider, registry

logger = logging.getLogger(__name__)


class LinkedInAdapter(ActionMessageProvider):
    id = 'linkedin_oauth2'
    name = 'LinkedInAdapter'

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.social_token = SocialToken.objects.filter(app__provider='linkedin_oauth2',
                                                       account__provider='linkedin_oauth2',
                                                       account__user=user)
        token = self.social_token.get()
        self.linked_in = linkedin.LinkedInApplication(token=linkedin.AccessToken(token.token, token.expires_at))
        self.social_app = SocialApp.objects.filter(id=token.app.id)

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
            logger.info('trying to create a likedIn update, for user: %s' % self.user)
            from django.utils.translation import ugettext as _

            result = self.linked_in.submit_share(
                message,
                "%s | %s" % (action_info.get('app', ''), action_info.get('action', '')),
                "%s %s %s %s %s" % (
                    action_info.get('actor', ''),
                    action_info.get('verb', ''),
                    action_info.get('target', ''),
                    _(u'using'),
                    action_info.get('app', _(u'application'))
                ),
                action_info.get('link', action_info.get('domain', '')),
                "%s%s" % (action_info.get('domain', ''), action_info['picture'].url) if 'picture' in action_info else ''
            )

            logger.info(str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e


registry.register(LinkedInAdapter)
