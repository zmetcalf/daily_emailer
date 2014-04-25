from django.conf.urls import patterns, url

urlpatterns = patterns('daily_emailer.views',
    url(r'^associated_emails/(?P<group_id>\d+)/$',
        'ajax_associated_emails'),
    url(r'^campaign_emails/(?P<campaign>\d+)/$',
        'ajax_campaign_emails'),
    url(r'^mustache_template/(?P<template>[a-zA-Z0-9_.-]+)$',
        'ajax_get_mustache_template'),
    url(r'^js_tests/', 'js_tests'),
)
