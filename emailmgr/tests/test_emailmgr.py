# -*- coding: utf-8 -*-
"""Unit tests for django bootup"""
from django.conf import settings
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from emailmgr.models import EmailAddress

class EmailTestCase(TestCase):
    """Tests for Django Mgr-Email - Default Superuser """
    
    def test_manager(self):
        pass

