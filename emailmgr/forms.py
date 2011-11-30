from models import EmailAddress
from django.forms import ModelForm
from django.conf import settings
from django.utils.translation import ugettext as _

class EmailAddressForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = EmailAddress
        exclude = ('user', 'is_primary', 'is_active', 'identifier')

    def clean_email(self):
        """
        Ensure this email address is unique throughout the ``site`` identified by SITE_ID.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email) or EmailAddress.objects.filter(email__iexact=email):
            msg = _("This email address is already in use.")
            raise forms.ValidationError(msg)

        return email
         