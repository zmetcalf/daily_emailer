from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from daily_emailer.models import Campaign, Email, SentEmail

def ajax_associated_emails(request, group_id):
    if not request.user.is_staff:
        raise Http404
    try:
        emails = Email.objects.all().filter(email_group_id=group_id)
    except Email.DoesNotExist:
        return HttpResponse('[]', content_type='application/json')
    data = serializers.serialize('json', emails)
    return HttpResponse(data, content_type='application/json')

def ajax_sent_emails(request, campaign):
    if not request.user.is_staff:
        raise Http404
    _campaign = get_object_or_404(Campaign, pk=campaign)
    emails = get_list_or_404(Email,
        email_group_id=_campaign.email_group.pk)

    sent_emails = SentEmail.objects.all().filter(campaign=_campaign)

    sent_emails_pks = []
    for se in sent_emails:
        sent_emails_pks.append(se.email.pk)

    email_list = []

    for email in emails:
        if email.pk in sent_emails_pks:
                email_list.append({ 'subject': email.subject,
                                    'sent_date': se.sent_date })
        else:
            email_list.append({ 'subject': email.subject })

    return render(request, 'daily_emailer/status.html',
                  { 'email_list': email_list })

def ajax_get_mustache_template(request, template):
    try:
        template = open('daily_emailer/templates/daily_emailer/mustache/{0}'.format(template), 'rb')
    except IOError:
        raise Http404
    return HttpResponse(template, content_type='text/plain')

def js_tests(request):
    return render(request, 'daily_emailer/js_tests.html')
