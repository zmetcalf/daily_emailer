import os

from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import render

from daily_emailer.models import Email


def ajax_associated_emails(request, group_id):
    if not request.user.is_staff:
        raise Http404
    try:
        emails = Email.objects.all().filter(email_group_id=group_id)
    except Email.DoesNotExist:
        return HttpResponse('[]', content_type='application/json')
    data = serializers.serialize('json', emails)
    return HttpResponse(data, content_type='application/json')


def ajax_get_mustache_template(request, template):
    try:
        template = open('{0}/daily_emailer/templates/daily_emailer/mustache/{1}'.format(
            os.path.dirname(os.path.dirname(__file__)), template), 'rb')
    except IOError:
        raise Http404
    return HttpResponse(template, content_type='text/plain')


def js_tests(request):
    return render(request, 'daily_emailer/js_tests.html')
