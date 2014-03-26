from django.test import TestCase
from django.test.client import Client

from daily_emailer.models import Email, EmailGroup

class AjaxAssociatedEmailTests(TestCase):

    def setUp(self):
        eq = EmailGroup(group_name='NewRep')
        eq.save()
        eq.email_set.create(subject='Subject1', message='Message1')
        eq.email_set.create(subject='Subject2', message='Message2')
        eq.email_set.create(subject='Subject3', message='Message3')
        eq.save()
        self.client = Client()

    def test_ajax_associated_emails(self):
        response = self.client.post('/associated_emails/1/')
        self.assertEqual(response.status_code, 200)
