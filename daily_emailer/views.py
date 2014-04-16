from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import  render

from daily_emailer.models import Campaign, Email

def ajax_associated_emails(request, group_id):
    if not request.user.is_staff:
        raise Http404
    try:
        emails = Email.objects.all().filter(email_group_id=group_id)
    except Email.DoesNotExist:
        return HttpResponse('[]', content_type='application/json')
    data = serializers.serialize('json', emails)
    return HttpResponse(data, content_type='application/json')

def ajax_campaign_emails(request, campaign):
    if not request.user.is_staff:
        raise Http404
    try:
        campaign = Campaign.objects.get(pk=campaign)
        emails = Email.objects.all().filter(
            email_group_id=campaign.email_group.pk)
    except (Email.DoesNotExist, Campaign.DoesNotExist):
        return HttpResponse('[]', content_type='application/json')
    data = serializers.serialize('json', emails)
    return HttpResponse(data, content_type='application/json')

def ajax_get_mustache_template(request, template):
    template = open('daily_emailer/templates/daily_emailer/mustache/{0}'.format(template), 'rb')
    return HttpResponse(template, content_type='text/plain')

def js_tests(request):
    return render(request, 'daily_emailer/js_tests.html')
