from django.contrib import admin

from apps.bookreader.models import Report, Reviews


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'fixed', 'added')

admin.site.register(Report, ReportAdmin)
admin.site.register(Reviews)