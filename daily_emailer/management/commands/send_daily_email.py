from django.core.management.base import BaseCommand, CommandError

from daily_emailer import models

class Command(BaseCommand):
    args = '<campaign_id campaign_id ...?'
    help = 'Handels sending out daily email'

    def handle(self, *args, **options):
        for campaign_id in args:
            try:
                campaign = models.Campaign.objects.get(pk=int(campaign_id))
            except models.Campaign.DeosNotExist:
                raise CommandError('Campaign "%s" does not exist' % campaign_id)

            if campaign.completed_date:
                return

            try:
                emails = Email.objects.all().filter(
                    email_group_id=campaign.email_group.pk)
            except Email.DoesNotExist:
                return # TODO Create test for this case

            email_order = list(map(int, campaign.email_group.email_order.strip('[]').split(',')))

            next_email = get_next_email(emails, email_order, campaign.status)

    def get_next_email(self, emails, email_order, sent_dict):
        for ordered_email in email_order:
            if not ordered_email in sent_dict.keys():
                for email in emails:
                    if email.pk == ordered_email:
                        return email
        return False
