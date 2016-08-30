from django.contrib import admin

from apps.bookrepo.models import Book, Creator, Contributor, Subject, MainSlider, BookPage


class BookAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'title', 'creator', 'subject', 'published', 'num_pages', 'num_copies',
                    'scanned', 'ebook')
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
                                    'ebook_file',
                                    ('published', 'num_pages'),
                                    ('is_panjabi'),
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


admin.site.register(Book, BookAdmin)
admin.site.register(Creator, admin.ModelAdmin)
admin.site.register(Contributor, admin.ModelAdmin)
admin.site.register(Subject, admin.ModelAdmin)
admin.site.register(MainSlider)
admin.site.register(BookPage)
