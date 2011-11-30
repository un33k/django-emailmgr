# -*- coding: utf-8 -*-
"""Unit tests for django bootup"""
from django.conf import settings
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from emailmgr.models import EmailAddress
from django.test.client import Client

class EmailTestCase(TestCase):
    """Tests for Django Mgr-Email - Default Superuser """
    def setUp(self):
        self.client = Client()

    def test_manager(self):
        response = self.client.post('/email/add/', {})
        response.status_code
        print response.status_code

