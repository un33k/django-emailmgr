from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages as Msg
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from forms import EmailAddressForm
from utils import send_activation, get_template

@login_required
def email_add(request):
    """
    User is logged and has a primary email address already
    This will add an aditional email address to this User
    """
    user = get_object_or_404(User, username__iexact=request.user.username)
    if request.method == 'POST':
        form = EmailAddressForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            Msg.add_message (request, messages.SUCCESS, _('email added'))
            return HttpResponseRedirect(reverse('emailmgr_list'))
    else:
        form = EmailAddressForm(user=user)

    return render_to_response(get_template('emailmgr_email_add.html'),
                              { 'form': form,},
                              context_instance=RequestContext(request)
                              )

@login_required
def email_delete(request, identifier="somekey"):
    user = get_object_or_404(User, username__iexact=request.user.username)
    email = get_object_or_404(EmailAddress, activation_key__iexact=identifier.lower())
    if email.email == user.email:
        Msg.add_message (request, messages.ERROR, _('cannot remove primary email address'))
    else:
        email.delete()
        Msg.add_message (request, messages.SUCCESS, _('email address removed'))

    return HttpResponseRedirect(reverse('emailmgr_list'))


@login_required
def email_make_primary(request, identifier="somekey"):
    user = get_object_or_404(User, username__iexact=request.user.username)
    email = get_object_or_404(EmailAddress, activation_key__iexact=identifier.lower())
    if email.is_active:
        if email_is_primary:
            Msg.add_message (request, messages.SUCCESS, _('email is already primary'))
        else:
            user.email = email.email
            email.is_primary = True
            Msg.add_message (request, messages.SUCCESS, _('primary address changed'))
    else:
        Msg.add_message (request, messages.SUCCESS, _('email must be activated first'))

    return HttpResponseRedirect(reverse('emailmgr_list'))


@login_required
def email_activate(request, identifier="somekey"):
    user = get_object_or_404(User, username__iexact=request.user.username)
    email = get_object_or_404(EmailAddress, activation_key__iexact=identifier.lower())
    if email.is_active:
        Msg.add_message (request, messages.SUCCESS, _('email already activated'))
    else:
        send_activation(identifier)
        Msg.add_message (request, messages.SUCCESS, _('activation email sent'))

    return HttpResponseRedirect(reverse('emailmgr_list'))








