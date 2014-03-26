from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from daily_emailer import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'daily_emailer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^associated_emails/(?P<group_id>\d+)/$',
        'daily_emailer.views.ajax_associated_emails'),
    url(r'^js_tests/', 'daily_emailer.views.js_tests'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
