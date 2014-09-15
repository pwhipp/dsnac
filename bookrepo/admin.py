from django.contrib import admin

import bookrepo.models as bm

admin.site.register(bm.Book, admin.ModelAdmin)
admin.site.register(bm.Creator, admin.ModelAdmin)
admin.site.register(bm.Contributor, admin.ModelAdmin)
admin.site.register(bm.Subject, admin.ModelAdmin)
