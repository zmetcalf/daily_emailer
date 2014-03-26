from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import  render

from daily_emailer.models import Email

def ajax_associated_emails(request, group_id):
    if not request.user.is_staff:
        raise Http404
    try:
        emails = Email.objects.all().filter(email_group_id=group_id)
    except Email.DoesNotExist:
        return HttpResponse('false', content_type='application/json')
    data = serializers.serialize('json', emails)
    return HttpResponse(data, content_type='application/json')

def js_tests(request):
    return render(request, 'daily_emailer/js_tests.html')
