# -*- coding: utf-8 -*-
"""Unit tests for django bootup"""
from django.conf import settings
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from emailmgr.models import EmailAddress
from django.test.client import Client
from django.core.urlresolvers import reverse
from emailmgr import forms
from django.contrib.auth import authenticate


class EmailTestCase(TestCase):
    """Tests for Django Mgr-Email - Default Superuser """
    def setUp(self):
        self.client = Client()

        #create a base test user
        self.user = User.objects.create_user('val', 'val@example.com', '1pass')
        
    def test_email_address_uniqueness(self):
        """
        Test & validates email addresses uniqueness
        """
        # create a user with an email address first
        user = User.objects.create_user('mike', 'mike@example.com', '2secret')

        # test against User.email
        # test a unique email address
        form = forms.EmailAddressForm(user=user, data={'email': 'john@example.com'})
        self.failUnless(form.is_valid())

        # test a duplicated email address
        form = forms.EmailAddressForm(user=user, data={'email': 'mike@example.com'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['email'],[u"This email address already in use."])

        # test against EmailAddress.email
        email = EmailAddress(**{'user': user, 'email': 'alvin@example.com'})
        email.save()
        
        # test a duplicated email address
        form = forms.EmailAddressForm(user=user, data={'email': 'alvin@example.com'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['email'],[u"This email address already in use."])

        # test a unique email address
        form = forms.EmailAddressForm(user=user, data={'email': 'sam@example.com'})
        self.failUnless(form.is_valid())


    def test_email_add(self):
        #import pdb; pdb.set_trace()
        retval = self.client.login(username='val', password='1pass')
        self.failUnless(retval)

        args = {'email': 'new1@example.com'}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertRedirects(response, reverse('emailmgr_email_list'))

        # make sure the email is saved
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==1)
        self.failUnless(e[0].email=='new1@example.com')

        # ensure duplicate email address are rejected
        args = {'email': 'new1@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertContains(response, "This email address already in use.", status_code=200)
        
        # ensure multiple emails per user are accepted
        args = {'email': 'new2@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertNotContains(response, "This email address already in use.", status_code=302)
        
        # make sure the email is in our database
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==2)
        self.failUnless(e[0].email=='new1@example.com')
        self.failUnless(e[1].email=='new2@example.com')
        self.failUnless(e[0].user==e[1].user)


    def test_email_list(self):
        # establish a session
        retval = self.client.login(username='val', password='1pass')
        self.failUnless(retval)

        # add few emails to user
        args = {'email': 'new1@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args) 
        self.assertNotContains(response, "This email address already in use.", status_code=302)

        args = {'email': 'new2@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertNotContains(response, "This email address already in use.", status_code=302)

        # verify that all emails were added
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==2)

        # list all email addresses
        response = self.client.post(reverse('emailmgr_email_list'))        
        self.assertNotContains(response, "This email address already in use.", status_code=200)
        self.assertContains(response, "example.com", count=len(e), status_code=200)
        self.assertContains(response, "Confirm Email", count=len(e), status_code=200)

        # make sure the option of adding new email is pased in to template
        self.assertContains(response, "id_email", count=2, status_code=200)


    def test_email_delete(self):
        # establish a session
        retval = self.client.login(username='val', password='1pass')
        self.failUnless(retval)

        # add few emails to user
        args = {'email': 'new1@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args) 
        self.assertNotContains(response, "This email address already in use.", status_code=302)

        args = {'email': 'new2@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertNotContains(response, "This email address already in use.", status_code=302)

        # verify that all emails were added
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==2)

        # delete the first email
        path = reverse('emailmgr_email_delete', kwargs={'identifier': e[0].identifier})
        response = self.client.get(path, follow=True)        
        self.assertContains(response, "example.com", count=1, status_code=200)
        self.assertContains(response, "Confirm Email", count=1, status_code=200)


