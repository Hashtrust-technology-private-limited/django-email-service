from django.contrib import admin
from email_service.models import Attachment,Template, Email
# Register your models here.

class EmailAdmin(admin.ModelAdmin):
    list_display = ['subject','from_user','state','scheduled_at','created_at']

admin.site.register(Email,EmailAdmin)
admin.site.register(Attachment)
admin.site.register(Template)
