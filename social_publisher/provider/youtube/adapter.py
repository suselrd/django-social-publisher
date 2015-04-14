#coding=utf-8
import httplib
import httplib2
import logging
import random
from allauth.socialaccount.models import SocialToken, SocialApp
from apiclient import discovery, http, errors
from oauth2client import GOOGLE_TOKEN_URI
from oauth2client.client import GoogleCredentials
import time
from social_publisher.provider import VideoProvider, registry

logger = logging.getLogger(__name__)

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error,
    IOError,
    httplib.NotConnected,
    httplib.IncompleteRead,
    httplib.ImproperConnectionState,
    httplib.CannotSendRequest,
    httplib.CannotSendHeader,
    httplib.ResponseNotReady,
    httplib.BadStatusLine
)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


class YoutubeAdapter(VideoProvider):
    id = 'youtube'
    name = 'YoutubeAdapter'

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
        self.youtube = discovery.build('youtube', 'v3', credentials=credentials)
        self.social_app = SocialApp.objects.filter(id=token.app.id)

    def publish_video(self, video, title='', description='', tags=None, private=True, **kwargs):

        try:
            logger.info('trying to publish youtube video, for user: %s' % self.user)

            insert_request = self.youtube.videos().insert(
                part='snippet,status',
                body=dict(
                    snippet=dict(
                        title=title,
                        description=description,
                        tags=tags
                    ),
                    status=dict(
                        privacyStatus='private' if private else 'public'
                    )
                ),
                media_body=http.MediaFileUpload(video.path, chunksize=-1, resumable=True)
            )
            result = self._resumable_upload(insert_request, title)

            logger.info(str(result))
            return result

        except Exception as e:
            logger.error(e)
            raise e

    def _resumable_upload(self, insert_request,  title):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                logger.info("Uploading file...")
                status, response = insert_request.next_chunk()
                if 'id' in response:
                    logger.info("'%s' (video id: %s) was successfully uploaded." % (title, response['id']))
                else:
                    logger.error("The upload failed with an unexpected response: %s" % response)
                    return response
            except errors.HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS, e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                logger.error(error)
                retry += 1
                if retry > MAX_RETRIES:
                    logger.error("No longer attempting to retry.")
                    return 'Upload Failed...'

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                logger.info("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

        return response


registry.register(YoutubeAdapter)
