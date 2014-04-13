from django.conf.urls import patterns, url

urlpatterns = patterns('daily_emailer.views',
    url(r'^associated_emails/(?P<group_id>\d+)/$',
        'ajax_associated_emails'),
    url(r'^campaign_emails/(?P<campaign>\d+)/$',
        'ajax_campaign_emails'),
    url(r'^js_tests/', 'js_tests'),
)
