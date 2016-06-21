from django.contrib import admin
from .models import Donate


class DonateAdmin(admin.ModelAdmin):
    list_display = ('user', 'added', 'amount')

admin.site.register(Donate, DonateAdmin)
