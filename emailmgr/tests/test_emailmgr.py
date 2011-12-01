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

        args = {'email': 'new@example.com'}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        
        print response

        EmailAddress.objects.all()
        
        # # # authenticate the user
        # # user = authenticate(username='val', password='1secret')
        # # self.failUnless(user)
        # #     
        # # # user is not authenticated yet, verify
        # # self.failUnless(self.user.is_authenticated())
        # # 
        # response = self.client.get(reverse('emailmgr_email_add'))
        # # 
        # #response = self.client.post('/login/', {'username': 'mike', 'password': '2secret'})
        # print response








