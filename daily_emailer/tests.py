import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.utils import timezone

from daily_emailer import models, fields
from daily_emailer.management.commands import send_daily_email

class AjaxAssociatedEmailTests(TestCase):

    def setUp(self):
        user = User.objects.create_user('Admin', 'admin@sample.com', 'password')
        user.is_staff = True
        user.save()
        eq = models.EmailGroup(group_name='NewRep')
        eq.save()
        eq.email_set.create(subject='Subject1', message='Message1')
        eq.email_set.create(subject='Subject2', message='Message2')
        eq.email_set.create(subject='Subject3', message='Message3')
        eq.save()
        self.client = Client()

    def test_ajax_associated_emails(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/associated_emails/1/')
        data = json.loads(response.content)
        self.assertEqual(data[0]['pk'], 1)
        self.assertEqual(data[0]['fields']['message'], 'Message1')
        self.assertEqual(data[1]['fields']['message'], 'Message2')
        self.assertEqual(data[2]['fields']['message'], 'Message3')

    def test_ajax_associated_emails_authenticated_empty(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/associated_emails/2/')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    def test_ajax_associated_emails_authenticated(self):
        self.client.login(username='Admin', password='password')
        response = self.client.post('/associated_emails/1/')
        self.assertEqual(response.status_code, 200)

    def test_ajax_associated_emails_unauthenticated(self):
        response = self.client.post('/associated_emails/1/')
        self.assertEqual(response.status_code, 404)

class StatusFieldTests(TestCase):

    def setUp(self):
        recipient = models.Recipient(first_name='John', last_name='Smith',
                                     email='sample@email.com')
        recipient.save()
        eq = models.EmailGroup(group_name='NewRep')
        eq.save()
        campaign = models.Campaign(reference_name='RefName',
                                   status='{1: "2014-4-1", 2: "2014-4-2"}',
                                   start_date=timezone.now(), email_group = eq,
                                   recipient = recipient)
        campaign.save()

    def test_status_field_to_python(self):
        email_history = models.Campaign.objects.all().filter(reference_name='RefName')
        self.assertEqual(email_history[0].status, {1: '2014-4-1', 2: '2014-4-2'})

class SendDailyEmailTests(TestCase):

    def setUp(self):
        eq = models.EmailGroup(group_name='NewRep', email_order='3,1,2')
        eq.save()
        eq.email_set.create(subject='Subject1', message='Message1')
        eq.email_set.create(subject='Subject2', message='Message2')
        eq.email_set.create(subject='Subject3', message='Message3')
        eq.save()
        self.cmd = send_daily_email.Command()

    def test_get_next_email(self):
        email_order = models.EmailGroup.objects.get(group_name='NewRep')
        emails = models.Email.objects.all().filter(email_group=email_order)
        self.assertEqual(self.cmd.get_next_email(emails, [3,1,2],
                         {3: '2014-4-1'}).pk, 1)
