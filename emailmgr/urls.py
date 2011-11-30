# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from views import email_add

# first thing first, let's take care of the homepage of the website first
urlpatterns = patterns('',
    url(r'^email/add$', email_add, name='emailmgr_email_add'),     
)