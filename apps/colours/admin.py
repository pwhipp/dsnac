from django.contrib import admin
from .models import Theme


class ThemeAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields

    # list_display = ['id', 'colour']

admin.site.register(Theme, ThemeAdmin)
