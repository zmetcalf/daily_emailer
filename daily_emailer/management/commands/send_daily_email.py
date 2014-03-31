import datetime

from django.core.management.base import BaseCommand, CommandError

from daily_emailer import models

class Command(BaseCommand):
    help = 'Handles sending out daily email'

    def handle_noargs(self):
        campaign_list = models.Campaign.objects.all()
        if not campaign_list:
            return

        for campaign in campaign_list:
            if campaign.completed_date:
                continue

            try:
                emails = models.Email.objects.all().filter(
                    email_group_id=campaign.email_group.pk)
            except models.Email.DoesNotExist:
                continue

            email_order = list(map(int, campaign.email_group.email_order.strip('[]').split(',')))

            if len(email_order) != len(email_order):
                email_order = self.reconcile_emails(emails,
                                campaign.email_group.email_order)
                campaign.email_group.email_order = email_order
                campaign.email_group.save()

            next_email = self.get_next_email(emails, email_order, campaign.status)

            if next_email:
                self.send_email(next_email, campaign.recipient)
                campaign.status[next_email.pk] = str(datetime.date.today())
            else:
                campaign.completed_date = datetime.date.today()
            campaign.save()

    # If user adds or removes an email before sorting, it needs fixed
    def reconcile_emails(self, emails, email_order):
        email_pk_list = []
        for email in emails:
            email_pk_list.append(email.pk)
            if not email.pk in email_order:
                email_order.append(email.pk)
        for list_item in email_order:
           if not list_item in email_pk_list:
              email_order.remove(list_item)
        return email_order

    # Algorithm to deterine next email to be sent
    def get_next_email(self, emails, email_order, sent_dict):
        for ordered_email in email_order:
            if not ordered_email in sent_dict.keys():
                for email in emails:
                    if email.pk == ordered_email:
                        return email
        return False

    def send_email(self, email, recipient):
        pass
