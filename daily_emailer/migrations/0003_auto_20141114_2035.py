# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daily_emailer', '0002_remove_campaign_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email_group',
            field=models.ForeignKey(related_name='email', to='daily_emailer.EmailGroup'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sentemail',
            name='campaign',
            field=models.ForeignKey(related_name='sent_email', to='daily_emailer.Campaign'),
            preserve_default=True,
        ),
    ]
