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

    sent_emails = get_list_or_404(SentEmail, campaign=_campaign)

    email_list = {}

    for email in emails:
        for se in sent_emails:
            if se.email == email:
                email_list[email] = { email.subject: se.sent_date }
                continue
        email_list[email] = { email.subject: '' }

    print email_list

    return render(request, 'daily_emailer/status.html', email_list)

def js_tests(request):
    return render(request, 'daily_emailer/js_tests.html')
