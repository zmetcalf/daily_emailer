from django.contrib import admin

from daily_emailer.models import Recipient, Email, EmailGroup, Campaign, \
                                 Attachment

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class EmailAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline,]

admin.site.register(Email, EmailAdmin)
admin.site.register([Recipient, EmailGroup, Campaign])

