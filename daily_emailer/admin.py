from django.contrib import admin
from django.template.loader import render_to_string

from daily_emailer import models


class AttachmentInline(admin.TabularInline):
    model = models.Attachment
    extra = 1


class EmailAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline, ]
    list_display = ('__str__', 'email_group')

    class Media:
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js',
            'daily_emailer/js/email.js',
            '//tinymce.cachefly.net/4.0/tinymce.min.js',
        )


class EmailGroupAdmin(admin.ModelAdmin):
    readonly_fields = ()
    exclude = ()

    class Media:
        css = {
            'all': (
                '//cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.4/css/jquery-ui.min.css',
                'daily_emailer/css/email-group.css',
            )
        }
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.6.0/underscore-min.js',
            '//cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min.js',
            '//cdnjs.cloudflare.com/ajax/libs/mustache.js/0.7.2/mustache.min.js',
            'daily_emailer/js/ordered_list.js',
            'daily_emailer/js/email_sort.js',
        )

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ()
        if not obj:
            self.exclude = ('email_order',)
        return super(EmailGroupAdmin, self).get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('id',)
        return self.readonly_fields


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'recipient', 'start_date', 'completed_date')
    exclude = ()
    readonly_fields = ()

    class Media:
        css = {
            'all': ('daily_emailer/css/campaign.css',)
        }

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('email_group', 'status', 'recipient',)
        return self.readonly_fields

    def status(self, instance):
        emails = models.Email.objects.all().filter(email_group_id=instance.email_group.pk)

        sent_emails = models.SentEmail.objects.all().filter(campaign=instance)
        sent_emails_pk = models.SentEmail.objects.all().filter(campaign=instance).values_list(
            'email__id', flat=True)

        email_list = []

        for email in emails:
            if email.pk in sent_emails_pk:
                for se in sent_emails:
                    if se.email == email:
                        email_list.append({'subject': email.subject,
                                           'sent_date': se.sent_date})
            else:
                email_list.append({'subject': email.subject})

        return render_to_string('daily_emailer/status.html',
                                {'email_list': email_list})

    status.allow_tags = True


class RecipientAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email')

admin.site.register(models.Email, EmailAdmin)
admin.site.register(models.EmailGroup, EmailGroupAdmin)
admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Recipient, RecipientAdmin)
