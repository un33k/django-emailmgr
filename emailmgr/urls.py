# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from views import email_add

#add an email to a User account
urlpatterns = patterns('',
    url(r'^email/add$', email_add, name='emailmgr_email_add'),     
)