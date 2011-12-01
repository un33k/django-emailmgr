from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from utils import get_unique_random

class EmailAddress(models.Model):

    user = models.OneToOneField(User, related_name="%(class)s", unique=True)
    email = models.EmailField(_("Email Address"))
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    identifier = models.CharField(max_length=255, default=get_unique_random(20).lower())

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        unique_together = (("user", "email"),)

    def __unicode__(self):
        return u"%s (%s)" % (self.email, self.user.username)


