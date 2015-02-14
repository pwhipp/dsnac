from django.contrib import admin

import bookrepo.models as bm


class BookAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'title', 'creator', 'subject', 'published', 'num_pages', 'num_copies', 'scanned', 'ebook')
    list_filter = ('creator', 'subject', 'scanned', 'ebook')
    search_fields = ('title',)
    fieldsets = ((None, {'fields': ('identifier',
                                    'title',
                                    'creator',
                                    'content',
                                    'subject',
                                    'contributor',
                                    'reference',
                                    'num_copies',
                                    'cover',
                                    'book_type',
                                    ('published', 'num_pages'),
                                    ('scanned', 'ebook'))}),
                 ('WebData', {'classes': ('collapse-closed',),
                              'fields': ('_meta_title',
                                         'slug',
                                         'short_url',
                                         'description',
                                         'gen_description',
                                         'keywords',
                                         'publish_date',
                                         'expiry_date')}))

admin.site.register(bm.Book, BookAdmin)
admin.site.register(bm.Creator, admin.ModelAdmin)
admin.site.register(bm.Contributor, admin.ModelAdmin)
admin.site.register(bm.Subject, admin.ModelAdmin)
admin.site.register(bm.MainSlider)
