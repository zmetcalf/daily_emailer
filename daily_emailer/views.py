from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404

from daily_emailer.models import Email

def ajax_associated_emails(request, group_id):
    if not request.user.is_staff:
        raise Http404
    emails = get_list_or_404(Email, email_group_id=group_id)
    data = serializers.serialize('json', emails)
    return HttpResponse(data, content_type='application/json')
