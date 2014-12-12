from distutils.core import setup

setup(
    name='django-social_publisher',
    version='0.3.0',
    packages=[
        'social_publisher',
        'social_publisher.provider',
        'social_publisher.provider.twitter',
        'social_publisher.provider.facebook',
        'social_publisher.provider.google'
    ],
    install_requires=[
        'django>=1.6.1',
        'django-allauth>=0.16.1',
        'twython>=3.2.0',
        'facebook-sdk>=1.0.0-alpha.1',
        'httplib2>=0.8',
        'oauth2client>=1.3',
        'uritemplate>=0.6',
        'google-api-python-client>=1.3.1'
    ],
    url='#',
    license='#',
    author='ernesto',
    author_email='jordan.ernesto@gmail.com',
    description='Application for posting in multiples social networks'
)
