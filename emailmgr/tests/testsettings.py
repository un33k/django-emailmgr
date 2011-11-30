import os
CUR_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = TEMPLATE_DEBUG = True
MAIN_DOMAIN_NAME = "example.com"
SITE_ID = 1
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': MAIN_DOMAIN_NAME.strip().split(".")[0]+"_db"
    }
}
INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'emailmgr',
]
ROOT_URLCONF = 'emailmgr.urls'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]


TEMPLATE_DIRS = os.path.join(CUR_DIR, "templates")


