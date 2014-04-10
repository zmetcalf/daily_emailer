import datetime

from django.core.management.base import BaseCommand, CommandError

from daily_emailer import models, utils

class Command(BaseCommand):
    args = 'Takes no arguments'
    help = 'Handles sending out daily email'

    def handle(self, *args, **options):
        campaign_list = models.Campaign.objects.all()
        if not campaign_list:
            return

        for campaign in campaign_list:
            if not self.get_ok_to_mail(campaign):
                continue

            emails = models.Email.objects.all().filter(
                    email_group_id=campaign.email_group.pk)

            if not emails:
                continue

            if campaign.email_group.email_order:
                email_order = list(map(int, campaign.email_group.email_order.strip('[]').split(',')))
            else:
                email_order = []

            email_order_sort = self.reconcile_emails(emails, list(email_order))

            if email_order_sort != email_order:
                email_order = email_order_sort
                campaign.email_group.email_order = str(email_order).strip('[]').replace(' ', '')
                campaign.email_group.save()

            next_email = self.get_next_email(emails, email_order, campaign.status)

            if next_email:
                utils.send_email(next_email, campaign.recipient)
                self.stdout.write(('Sent {0} to {1} {2} at {3}\n'.format(
                            next_email.subject,
                            campaign.recipient.first_name,
                            campaign.recipient.last_name,
                            campaign.recipient.email)))
                campaign.status[int(next_email.pk)] = str(datetime.date.today())
            else:
                campaign.completed_date = datetime.date.today()
            campaign.save()

    # Check to see if completd or already sent that day
    def get_ok_to_mail(self, campaign):
        if campaign.completed_date:
            return False

        if not campaign.status:
            if (campaign.start_date - datetime.date.today()).days <= 0:
                return True
            else:
                return False

        last_date = datetime.date(1970, 1, 1)
        for key, value in campaign.status.iteritems():
            _value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            if (last_date - _value).days < 0:
                last_date = _value

        if (last_date  - datetime.date.today()).days >= 0:
            return False
        else:
            return True

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
