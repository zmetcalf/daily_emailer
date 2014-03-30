from django.contrib import admin

from daily_emailer import models

class AttachmentInline(admin.TabularInline):
    model = models.Attachment
    extra = 1

class EmailAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline,]

class EmailGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

    class Media:
        css = {
            'all': ('//cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.4/css/jquery-ui.min.css',)
        }
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.6.0/underscore-min.js',
            '//cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min.js',
            '//cdnjs.cloudflare.com/ajax/libs/mustache.js/0.7.2/mustache.min.js',
            'js/ordered_list.js',
            'js/email_sort.js',
        )

class CampaignAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

    class Media:
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js',
            'js/campaign.js',
        )

admin.site.register(models.Email, EmailAdmin)
admin.site.register(models.EmailGroup, EmailGroupAdmin)
admin.site.register(models.Campaign, CampaignAdmin)
admin.site.register(models.Recipient)
