# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=50)),
                ('attachment', models.FileField(upload_to=b'email_attachments/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=1, blank=True)),
                ('reference_name', models.CharField(max_length=128)),
                ('start_date', models.DateField()),
                ('completed_date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=77)),
                ('message', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=50)),
                ('email_order', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(unique=True, max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SentEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent_date', models.DateField()),
                ('campaign', models.ForeignKey(to='daily_emailer.Campaign')),
                ('email', models.ForeignKey(to='daily_emailer.Email')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='email',
            name='email_group',
            field=models.ForeignKey(to='daily_emailer.EmailGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='email_group',
            field=models.ForeignKey(to='daily_emailer.EmailGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='recipient',
            field=models.ForeignKey(to='daily_emailer.Recipient'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='email',
            field=models.ForeignKey(to='daily_emailer.Email'),
            preserve_default=True,
        ),
    ]
