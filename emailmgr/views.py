from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages as Msg
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from forms import EmailAddressForm
from models import EmailAddress
from utils import send_activation, get_template
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


@login_required
def email_add(request):
    """
    User is logged and has a primary email address already
    This will add an aditional email address to this User
    """
    if request.method == 'POST':
        form = EmailAddressForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            Msg.add_message (request, Msg.SUCCESS, _('email address added'))
            return HttpResponseRedirect(reverse('emailmgr_email_list'))
    else:
        form = EmailAddressForm(user=request.user)

    return render_to_response(get_template('emailmgr_email_add.html'),
                              {'add_email_form': form},
                              context_instance=RequestContext(request)
                              )

@login_required
def email_delete(request, identifier="somekey"):
    email = get_object_or_404(EmailAddress, identifier__iexact=identifier.lower())
    if email.email == request.user.email:
        Msg.add_message (request, Msg.ERROR, _('cannot remove primary email address'))
    elif email.user != request.user:
        Msg.add_message (request, Msg.ERROR, _('email address is not associated with this account'))
    else:
        email.delete()
        Msg.add_message (request, Msg.SUCCESS, _('email address removed'))

    return HttpResponseRedirect(reverse('emailmgr_email_list'))


@login_required
def email_make_primary(request, identifier="somekey"):
    email = get_object_or_404(EmailAddress, identifier__iexact=identifier.lower())
    if email.is_active:
        if email.is_primary:
            Msg.add_message (request, Msg.SUCCESS, _('email address is already primary'))
        else:
            request.user.email = email.email
            request.user.save()
            email.is_primary = True
            email.save()
            Msg.add_message (request, Msg.SUCCESS, _('primary address changed'))
    else:
        Msg.add_message (request, Msg.SUCCESS, _('email address must be activated first'))

    return HttpResponseRedirect(reverse('emailmgr_email_list'))


@login_required
def email_activate(request, identifier="somekey"):
    email = get_object_or_404(EmailAddress, identifier__iexact=identifier.lower())
    if email.is_active:
        Msg.add_message (request, Msg.SUCCESS, _('email address already active'))
    else:
        email.is_active = True
        email.save()
        Msg.add_message (request, Msg.SUCCESS, _('email address is now active'))

    return HttpResponseRedirect(reverse('emailmgr_email_list'))


@login_required
def email_send_activation(request, identifier="somekey"):
    email = get_object_or_404(EmailAddress, identifier__iexact=identifier.lower())
    if email.is_active:
        Msg.add_message (request, Msg.SUCCESS, _('email address already activated'))
    else:
        send_activation(identifier)
        Msg.add_message (request, Msg.SUCCESS, _('activation email sent'))

    return HttpResponseRedirect(reverse('emailmgr_email_list'))


@login_required
def email_list(request):
    
    email_add_form = EmailAddressForm(user=request.user)
    emails_list = EmailAddress.objects.all()
    return render_to_response(get_template('emailmgr_email_list.html'),
                              {
                                'emails_list': emails_list,
                                'add_email_form': email_add_form
                              },
                              context_instance=RequestContext(request)
                              )










