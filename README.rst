==========================
Django Social Publisher
==========================
The main idea of this application is create contents in multiples social networks.

Changelog
=========
0.1.0
-----
+ Initial idea.
+ Posting in facebook(image, video and status messages) and twitter(update status, and update status with an image)
+ Add simple example

Notes
-----

PENDING...

Usage
-----

1. Run ``python setup.py install`` to install.

2. set in your django-allauth settings SOCIALACCOUNT_PROVIDERS for permission request(in facebook)
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['photo_upload',
                  'publish_actions',
                  'publish_stream',
                  'read_stream',
                  'share_item',
                  'status_update',
                  'video_upload',
                  'create_event',
                  'user_birthday',
                  'user_likes',
                  'user_videos',
                  'create_event',
                  'user_photos'
        ]},
}
3. Check the write permission of twitter app.
4. Add publishers settings
PUBLISHERS = (
    'social_publisher.provider.facebook',
    'social_publisher.provider.twitter',
)
5. Configure social networks, they are the link bettwen django-allauth and publisher providers

6. When you create new content in your site and you want to notify using social networks:
   take present to ways:
   1-using current user social accounts
   2-using site account or a business account (this need additional setting,
     set SITE_OWNER in you settings to the user id owner of the site accounts)