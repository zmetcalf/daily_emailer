from django.contrib import admin

from daily_emailer.models import Recipient, Email, EmailGroup, Campaign, \
                                 Attachment

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class EmailAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline,]

class EmailGroupAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('//cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.4/css/jquery-ui.min.css',)
        }
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/mustache.js/0.7.2/mustache.min.js',
            'js/email_sort.js',
        )

admin.site.register(Email, EmailAdmin)
admin.site.register(EmailGroup, EmailGroupAdmin)
admin.site.register([Recipient, Campaign])

