# -*- coding: utf-8 -*-
"""Unit tests for django bootup"""
from django.conf import settings
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from emailmgr.models import EmailAddress
from django.test.client import Client
from emailmgr import forms

class EmailTestCase(TestCase):
    """Tests for Django Mgr-Email - Default Superuser """
    def setUp(self):
        #create a base test user
        User.objects.create_user('val', 'val@example.com', '1secret')

        self.client = Client()

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
        self.assertEqual(form.errors['email'],[u"Email address is already in use."])

        # test against EmailAddress.email
        email = EmailAddress(**{'user': user, 'email': 'alvin@example.com'})
        email.save()
        
        # test a duplicated email address
        form = forms.EmailAddressForm(user=user, data={'email': 'alvin@example.com'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['email'],[u"Email address is already in use."])

        # test a unique email address
        form = forms.EmailAddressForm(user=user, data={'email': 'sam@example.com'})
        self.failUnless(form.is_valid())


