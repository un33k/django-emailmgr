import os, random, string, time
from django.conf import settings
from django.db import models, IntegrityError
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
from django.utils.translation import gettext_lazy as _
import defaults

def send_activation(identitifer):
    current_site = Site.objects.get_current()


# get a random string of known length
def get_unique_random(length=10):
    randtime = str(time.time()).split('.')[0]
    rand = ''.join([random.choice(randtime+string.letters+string.digits) for i in range(length)])
    return sha_constructor(rand).hexdigest()[:length]
 
# given a template name, return its path
def get_template(name):
    return os.path.join(getattr(defaults, "EMAIL_MGR_TEMPLATE_PATH"), name)





