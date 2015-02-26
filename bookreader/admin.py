from django.contrib import admin

from bookreader.models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'fixed', 'added')

admin.site.register(Report, ReportAdmin)