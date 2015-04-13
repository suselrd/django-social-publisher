==========================
Django Social Publisher
==========================
The main idea of this application is create content in multiples social networks.

Changelog
=========
0.3.6
-----
+ Added a template tag to obtain the enabled social networks by content. (ex: 'video', 'image', 'message', 'action_message')

0.3.5
-----
+ Added specific context processors values

0.3.4
-----
+ Added Migrations. (To update to this version, you must first run 'manage.py migrate social_publisher 0001 --fake')
+ Removed unique constraint for social_app FK in SocialNetworkApp model. (Then run 'manage.py migrate social_publisher')

0.3.3
-----
+ New channel: Youtube (VideoProvider). Post videos in Youtube.

0.3.2
-----
+ Fixed kwargs modifications in facebook adapter.

0.3.1
-----
+ Spanish translations files.

0.3.0
-----
+ New type of content to publish: ActionMessage
+ New channel: Google+ (ActionMessageProvider). Creates Moments in Google+.
+ New channel: LinkedIn (ActionMessageProvider). Shares updates in LinkedIn.

0.2.0
-----
+ Included some changes to support multi-site behavior.
+ The SocialNetwork class could be related with more than one SocialApp. Added a new class named 'SocialNetworkApp'
to establish the relationship between both classes.

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

2. Configure your social accounts providers (django-allauth setting SOCIALACCOUNT_PROVIDERS)
3. Make sure yoy set the necessary scopes/permissions to write posts to your social networks.
4. Add publishers settings
PUBLISHERS = (
    'social_publisher.provider.facebook',
    'social_publisher.provider.twitter',
)
5. Configure social networks, they are the link between django-allauth and publisher providers

6. When you create new content in your site and you want to notify using social networks:
   take present to ways:
   1-using current user social accounts
   2-using site account or a business account (this need additional setting,
     set SITE_OWNER in you settings to the user id owner of the site accounts)