# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from views import email_add, email_list

#add an email to a User account
urlpatterns = patterns('',
    url(r'^email/add$', email_add, name='emailmgr_email_add'),     
    url(r'^email/list$', email_list, name='emailmgr_email_list'),     
)