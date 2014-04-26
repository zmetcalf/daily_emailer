# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from daily_emailer.models import Campaign, Email, SentEmail

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SentEmail'
        db.create_table(u'daily_emailer_sentemail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['daily_emailer.Email'])),
            ('sent_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['daily_emailer.Campaign'])),
        ))
        db.send_create_signal(u'daily_emailer', ['SentEmail'])

        self.forward_migrate_status()


    def backwards(self, orm):

        self.backward_migrate_status()

        # Deleting model 'SentEmail'
        db.delete_table(u'daily_emailer_sentemail')


    def forward_migrate_status(self):
        campaign_list = Campaign.objects.all()
        if campaign_list:
            for _campaign in campaign_list:
                for key, value in _campaign.status.iteritems():
                    _email = Email.objects.get(pk=key)
                    SentEmail(email=_email, sent_date=value, campaign=_campaign)


    def backward_migrate_status(self):
        campaign_list = Campaign.objects.all()
        if campaign_list:
            for _campaign in campaign_list:
                sent_email_list = SentEmail.objects.all().filter(campaign=_campaign)
                if sent_email_list:
                    for email in sent_email_list:
                        _campaign.status[int(email.email.pk)] = email.sent_date


    models = {
        u'daily_emailer.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['daily_emailer.Email']"}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'daily_emailer.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'completed_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['daily_emailer.EmailGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['daily_emailer.Recipient']"}),
            'reference_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'status': ('daily_emailer.fields.StatusField', [], {'null': 'True', 'blank': 'True'})
        },
        u'daily_emailer.email': {
            'Meta': {'object_name': 'Email'},
            'email_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['daily_emailer.EmailGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '77'})
        },
        u'daily_emailer.emailgroup': {
            'Meta': {'object_name': 'EmailGroup'},
            'email_order': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'daily_emailer.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'daily_emailer.sentemail': {
            'Meta': {'object_name': 'SentEmail'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['daily_emailer.Campaign']"}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['daily_emailer.Email']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['daily_emailer']
