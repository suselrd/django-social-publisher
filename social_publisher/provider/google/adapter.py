#coding=utf-8
import logging
from allauth.socialaccount.models import SocialToken, SocialApp
from apiclient import discovery
from oauth2client import GOOGLE_TOKEN_URI
from oauth2client.client import GoogleCredentials
from social_publisher.provider import ActionMessageProvider, registry

logger = logging.getLogger(__name__)


class GoogleAdapter(ActionMessageProvider):
    id = 'google'
    name = 'GoogleAdapter'

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.social_token = SocialToken.objects.filter(app__provider='google',
                                                       account__provider='google',
                                                       account__user=user)
        token = self.social_token.get()
        credentials = GoogleCredentials(
            access_token=token.token,
            client_id=token.app.client_id,
            client_secret=token.app.secret,
            refresh_token=token.token_secret,
            token_expiry=token.expires_at,
            token_uri=GOOGLE_TOKEN_URI,
            user_agent=None
        )
        self.google = discovery.build('plus', 'v1', credentials=credentials)
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
            logger.info('trying to create a google moment, for user: %s' % self.user)

            link = action_info.get('link', None)
            if link:
                moment = {
                    "type": "http://schema.org/AddAction",
                    "target": {
                        "url": link,
                    }
                }
            else:
                from datetime import datetime
                moment = {
                    "type": "http://schema.org/AddAction",
                    "target": {
                        "id": "%s" % datetime.now().isoformat(),
                        "type": "http://schema.org/AddAction",
                        "name": action_info.get('target'),
                        "description": "%s %s %s" % (
                            action_info.get('actor', ''),
                            action_info.get('verb', ''),
                            action_info.get('target', '')
                        ),
                        "image": "%s%s" % (action_info.get('domain', ''), action_info['picture'].url) if 'picture' in action_info else ''
                    }
                }

            google_request = self.google.moments().insert(userId='me', collection='vault', body=moment)
            result = google_request.execute()

            logger.info(str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e


registry.register(GoogleAdapter)
